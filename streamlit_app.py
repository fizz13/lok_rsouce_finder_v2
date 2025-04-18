import streamlit as st
import requests
import pandas as pd
from collections import Counter

st.set_page_config(page_title="LOK Resource Finder", page_icon="🪨")
st.title("🪨 League of Kingdoms – Resource Finder")

with st.form("finder_form"):
    token = st.text_input("🔑 Access Token", type="password")
    continent = st.number_input("🌍 Continent", value=70)
    x = st.number_input("📍 Tọa độ X", value=900)
    y = st.number_input("📍 Tọa độ Y", value=1130)
    min_level = st.slider("📏 Level tối thiểu", 1, 5, 2)
    resource_types = st.multiselect("🧪 Loại tài nguyên", ["DSA", "Crystal"], default=["DSA", "Crystal"])
    submitted = st.form_submit_button("🔍 Tìm mỏ")

if submitted:
    with st.spinner("⏳ Đang truy vấn dữ liệu từ LOK BOT..."):
        url = "https://lok-api.lokbot.co/api/v1/finder/zones"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "x": x,
            "y": y,
            "continent": continent,
            "min_level": min_level,
            "resource": resource_types
        }

        try:
            res = requests.post(url, headers=headers, json=payload, timeout=15)
            if res.status_code == 200:
                data = res.json()
                nodes = data.get("data", [])

                if not nodes:
                    st.warning("⚠️ Không tìm thấy mỏ nào phù hợp.")
                else:
                    st.success(f"✅ Tìm thấy {len(nodes)} mỏ")

                    # Hiển thị từng mỏ
                    for node in nodes:
                        st.write(f"🪨 {node['resource']} Lv{node['level']} tại tọa độ **({node['x']}, {node['y']})**")

                    # Thống kê
                    type_counts = Counter(node['resource'] for node in nodes)
                    st.markdown("### 📊 Thống kê:")
                    for rtype, count in type_counts.items():
                        st.markdown(f"- **{rtype}**: {count} mỏ")

                    # Xuất CSV
                    df = pd.DataFrame(nodes)[["resource", "level", "x", "y"]]
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Tải danh sách mỏ (.CSV)",
                        data=csv,
                        file_name="lok_resources.csv",
                        mime='text/csv'
                    )
            else:
                st.error(f"❌ API trả về lỗi: {res.status_code}\n{res.text}")

        except Exception as e:
            st.error(f"❌ Lỗi khi gọi API: {e}")
