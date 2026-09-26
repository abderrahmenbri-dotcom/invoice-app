import streamlit as st
import pandas as pd

# تهيئة قائمة الفواتير في ذاكرة الجلسة
if 'invoices' not in st.session_state:
    st.session_state.invoices = []

st.title("🧾 نظام الفواتير وتصدير Excel")
st.write("قم بإدخال بيانات الفاتورة، وحفظها، ثم تحميل كافة الفواتير في ملف Excel.")

# نموذج إدخال بيانات الفاتورة
with st.form("invoice_form"):
    col1, col2 = st.columns(2)
    with col1:
        store_name = st.text_input("اسم المحل / المتجر", "متجر الأناقة")
        customer_name = st.text_input("اسم الزبون", "أحمد علي")
    with col2:
        product_name = st.text_input("اسم المنتج / الخدمة", "قميص رجالي")
        price = st.number_input("سعر الوحدة", min_value=0.0, value=150.0)
        quantity = st.number_input("الكمية", min_value=1, value=1)
    
    submit_button = st.form_submit_button("إضافة الفاتورة")

# عند الضغط على زر إضافة الفاتورة
if submit_button:
    total_price = price * quantity
    new_invoice = {
        "اسم المتجر": store_name,
        "اسم الزبون": customer_name,
        "المنتج": product_name,
        "سعر الوحدة": price,
        "الكمية": quantity,
        "المجموع الإجمالي": total_price
    }
    st.session_state.invoices.append(new_invoice)
    st.success(f"تمت إضافة فاتورة الزبون ({customer_name}) بنجاح!")

# عرض جدول الفواتير المسجلة وخيار التحميل
if st.session_state.invoices:
    st.divider()
    st.subheader("📋 قائمة الفواتير المسجلة")
    
    # تحويل البيانات إلى الجدول (DataFrame)
    df = pd.DataFrame(st.session_state.invoices)
    st.dataframe(df, use_container_width=True)
    
    # تحويل جدول البيانات إلى ملف Excel في الذاكرة
    import io
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='الفواتير')
    
    # زر تنزيل ملف Excel
    st.download_button(
        label="📥 تحميل الفواتير كملف Excel",
        data=buffer.getvalue(),
        file_name="invoices_summary.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )