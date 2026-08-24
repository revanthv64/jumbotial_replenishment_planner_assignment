import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title='Replenishment Planner', page_icon='📦', layout='wide')
DATA_FILE = Path(__file__).parent / 'final_replenishment_data.csv'

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    numeric_cols = [
        'vendor_lead_time','inv_norm','safety_stock','max_allocated_space',
        'case_size','cases_allocated','space_value','current_inventory','max_drr',
        'deadweight','orderedquantity','open_po_value','open_po_cases',
        'final_suggestion','final_days_of_inventory','final_cases_suggestion',
        'final_value','final_tonnage','mrp','cp','current_days_raw',
        'inventory_position','target_days','target_units','raw_replenishment',
        'residual_capacity','max_order_cases','desired_cases','mov_required_cases',
        'projected_inventory'
    ]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
    return df

try:
    df = load_data(DATA_FILE)
except FileNotFoundError:
    st.error(f'Could not find {DATA_FILE.name}. Put the CSV in the same folder as app.py.')
    st.stop()

# ---------------- Inventory health ----------------
def health(row):
    drr = row.get('max_drr', 0)
    doi = row.get('current_days_raw', 0)
    target = row.get('target_days', 0)
    if drr <= 0:
        return 'No Demand'
    if doi <= 0:
        return 'Stockout'
    if target > 0 and doi < target:
        return 'Understock'
    if target > 0 and doi <= target * 1.5:
        return 'Healthy'
    return 'Overstock'

df['inventory_health'] = df.apply(health, axis=1)

# ---------------- Sidebar ----------------
st.sidebar.title('🔎 Planner Filters')

filtered = df.copy()

def multiselect_filter(label, column):
    global filtered
    if column in filtered.columns:
        values = sorted(filtered[column].dropna().astype(str).unique().tolist())
        selected = st.sidebar.multiselect(label, values, default=values)
        if selected:
            filtered = filtered[filtered[column].astype(str).isin(selected)]

multiselect_filter('Facility', 'facility_name')
multiselect_filter('Sales Band', 'sales_band')

if 'inventory_health' in filtered.columns:
    values = ['Stockout', 'Understock', 'Healthy', 'Overstock', 'No Demand']
    values = [v for v in values if v in filtered['inventory_health'].unique()]
    selected = st.sidebar.multiselect('Inventory Health', values, default=values)
    if selected:
        filtered = filtered[filtered['inventory_health'].isin(selected)]

multiselect_filter('Vendor', 'vendor_name')
multiselect_filter('Category', 'category_name')

st.sidebar.divider()
st.sidebar.caption(f'Showing {len(filtered):,} of {len(df):,} SKUs')

# ---------------- Header ----------------
st.title('📦 Replenishment Planner')
st.caption('Inventory Health • Replenishment Prioritization • Vendor & PO Analysis')

# ---------------- KPIs ----------------
need_po = (filtered['final_suggestion'] > 0).sum()
po_value = filtered['final_value'].sum()
suggested_cases = filtered['final_cases_suggestion'].sum()
avg_doi = filtered['current_days_raw'].mean()
open_po_value = filtered['open_po_value'].sum()
at_risk = filtered['inventory_health'].isin(['Stockout', 'Understock']).sum()

k = st.columns(6)
k[0].metric('Total SKUs', f'{len(filtered):,}')
k[1].metric('Need Replenishment', f'{need_po:,}')
k[2].metric('Suggested PO Value', f'₹{po_value:,.0f}')
k[3].metric('Suggested Cases', f'{suggested_cases:,.0f}')
k[4].metric('Average DOI', f'{avg_doi:.1f}')
k[5].metric('At Risk', f'{at_risk:,}')

st.divider()

# ---------------- Inventory health ----------------
st.subheader('📊 Inventory Health')
health_summary = filtered['inventory_health'].value_counts().reindex(
    ['Stockout', 'Understock', 'Healthy', 'Overstock', 'No Demand'], fill_value=0
)
a, b = st.columns([1.2, 1])
with a:
    st.bar_chart(health_summary)
with b:
    st.dataframe(
        health_summary.rename('SKU Count').reset_index().rename(columns={'index': 'Inventory Health'}),
        use_container_width=True, hide_index=True
    )

# ---------------- Priority replenishment ----------------
st.divider()
st.subheader('🚨 Priority Replenishment')
priority = filtered[filtered['final_suggestion'] > 0].copy()
band_map = {'A': 1, 'B': 2, 'C': 3}
priority['_band_priority'] = priority['sales_band'].astype(str).str.upper().map(band_map).fillna(4)
priority = priority.sort_values(
    ['_band_priority', 'current_days_raw', 'final_value'],
    ascending=[True, True, False]
)
priority_cols = [
    'facility_name','jpin','title','sales_band','max_drr','current_inventory',
    'current_days_raw','target_days','open_po_cases','final_cases_suggestion','final_value'
]
st.dataframe(priority[priority_cols].head(100), use_container_width=True, hide_index=True)

# ---------------- SKU detail ----------------
st.divider()
st.subheader('🔍 SKU Detail')
skus = filtered['jpin'].dropna().astype(str).unique().tolist()
if skus:
    selected_sku = st.selectbox('Select SKU', skus)
    row = filtered[filtered['jpin'].astype(str) == selected_sku].iloc[0]
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('### Product')
        st.write(f"**Product:** {row['title']}")
        st.write(f"**Facility:** {row['facility_name']}")
        st.write(f"**Vendor:** {row['vendor_name']}")
        st.write(f"**Sales Band:** {row['sales_band']}")
        st.write(f"**Inventory Health:** {row['inventory_health']}")
    with c2:
        st.markdown('### Replenishment')
        st.write(f"**Current Inventory:** {row['current_inventory']:,.0f}")
        st.write(f"**Current DOI:** {row['current_days_raw']:.1f} days")
        st.write(f"**Target DOI:** {row['target_days']:.1f} days")
        st.write(f"**DRR:** {row['max_drr']:.2f}")
        st.write(f"**Open PO:** {row['open_po_cases']:,.0f} cases")
        st.write(f"**Suggested Order:** {row['final_cases_suggestion']:,.0f} cases")
        st.write(f"**Suggested Value:** ₹{row['final_value']:,.0f}")

    st.markdown('### Why this SKU is being considered')
    reasons = []
    if row['inventory_health'] == 'Stockout':
        reasons.append('🔴 Current inventory is at stockout level.')
    elif row['inventory_health'] == 'Understock':
        reasons.append('🟠 Current DOI is below target DOI.')
    elif row['inventory_health'] == 'Overstock':
        reasons.append('🟡 Current inventory is above the target level.')
    if str(row['sales_band']).upper() == 'A':
        reasons.append('⭐ Sales Band A — high-priority SKU.')
    if row['open_po_cases'] > 0:
        reasons.append(f"🚚 {row['open_po_cases']:,.0f} open PO cases are already in the pipeline.")
    if str(row['mov_check']).upper() == 'PASS':
        reasons.append('✅ MOV requirement passed.')
    elif str(row['mov_check']).upper() == 'FAIL':
        reasons.append('⚠️ MOV requirement failed.')
    if row['residual_capacity'] <= 0:
        reasons.append('⚠️ Residual warehouse capacity is constrained.')
    for reason in reasons or ['ℹ️ No specific exception identified.']:
        st.write(reason)

# ---------------- Sales band ----------------
st.divider()
st.subheader('📈 Sales Band Analysis')
sales_summary = filtered.groupby('sales_band').agg(
    SKU_Count=('jpin','size'),
    Average_DOI=('current_days_raw','mean'),
    Replenishment_Value=('final_value','sum'),
    Suggested_Cases=('final_cases_suggestion','sum')
).reset_index()
a, b = st.columns(2)
with a:
    st.dataframe(sales_summary, use_container_width=True, hide_index=True)
with b:
    st.bar_chart(sales_summary.set_index('sales_band')['Replenishment_Value'])

# ---------------- Vendor ----------------
st.divider()
st.subheader('🏭 Vendor Analysis')
vendor_summary = filtered.groupby('vendor_name').agg(
    SKU_Count=('jpin','size'),
    Average_Lead_Time=('vendor_lead_time','mean'),
    Replenishment_Value=('final_value','sum'),
    Suggested_Cases=('final_cases_suggestion','sum')
).reset_index().sort_values('Replenishment_Value', ascending=False)
st.dataframe(vendor_summary.head(25), use_container_width=True, hide_index=True)

# ---------------- Open PO / MOV ----------------
st.divider()
a, b = st.columns(2)
with a:
    st.subheader('🚚 Open PO Exposure')
    open_po = filtered[filtered['open_po_value'] > 0]
    st.metric('SKUs With Open PO', f'{len(open_po):,}')
    st.metric('Open PO Value', f'₹{open_po["open_po_value"].sum():,.0f}')
    cols = ['facility_name','jpin','title','vendor_name','open_po_cases','open_po_value']
    st.dataframe(open_po[cols].head(25), use_container_width=True, hide_index=True)
with b:
    st.subheader('📦 MOV Exceptions')
    mov_fail = filtered[filtered['mov_check'].astype(str).str.upper() == 'FAIL']
    st.metric('MOV Failures', f'{len(mov_fail):,}')
    cols = ['facility_name','vendor_name','jpin','title','minimum_order_criteria','current_vendor_mov','mov_required_cases','final_cases_suggestion','mov_check']
    st.dataframe(mov_fail[cols].head(25), use_container_width=True, hide_index=True)

# ---------------- Export ----------------
st.divider()
st.subheader('⬇️ Export')
st.download_button(
    'Download Filtered Replenishment Data',
    filtered.to_csv(index=False),
    file_name='filtered_replenishment_output.csv',
    mime='text/csv'
)
