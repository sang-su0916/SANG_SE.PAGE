import streamlit as st
import json
from datetime import datetime
import base64
import zipfile
import io
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="AI 상세페이지 생성기",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 5px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #5a5fcf;
        transform: translateY(-2px);
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# 상세페이지 생성 함수
def generate_detail_page(product_info):
    """주어진 정보로 HTML 상세페이지 생성"""
    
    # 카테고리별 템플릿 스타일
    templates = {
        "전자제품": {
            "primary_color": "#2196F3",
            "secondary_color": "#1976D2",
            "style": "modern"
        },
        "패션": {
            "primary_color": "#E91E63",
            "secondary_color": "#C2185B",
            "style": "elegant"
        },
        "뷰티": {
            "primary_color": "#FF6B6B",
            "secondary_color": "#FFA07A",
            "style": "soft"
        },
        "경영경제서적": {
            "primary_color": "#2C3E50",
            "secondary_color": "#3498DB",
            "style": "professional"
        },
        "식품": {
            "primary_color": "#4CAF50",
            "secondary_color": "#388E3C",
            "style": "fresh"
        },
        "기타": {
            "primary_color": "#9C27B0",
            "secondary_color": "#7B1FA2",
            "style": "creative"
        }
    }
    
    template = templates.get(product_info.get('category', '기타'), templates['기타'])
    
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product_info['product_name']} - AI 생성 상세페이지</title>
    <meta name="description" content="{product_info.get('description', '')}">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary-color: {product_info.get('brand_color', template['primary_color'])};
            --secondary-color: {template['secondary_color']};
            --text-dark: #2C3E50;
            --text-light: #7F8C8D;
            --bg-light: #F8F9FA;
        }}
        
        body {{
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-dark);
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        /* Hero Section */
        .hero {{
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            padding: 100px 0;
            text-align: center;
        }}
        
        .hero h1 {{
            font-size: 3em;
            margin-bottom: 20px;
            font-weight: 700;
        }}
        
        .hero .price {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 20px 0;
        }}
        
        .hero .description {{
            font-size: 1.3em;
            margin-bottom: 40px;
            opacity: 0.9;
        }}
        
        .cta-button {{
            display: inline-block;
            background: white;
            color: var(--primary-color);
            padding: 15px 40px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: 600;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }}
        
        /* Features Section */
        .features {{
            padding: 80px 0;
            background: white;
        }}
        
        .section-title {{
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 20px;
            color: var(--primary-color);
        }}
        
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
            margin-top: 60px;
        }}
        
        .feature-card {{
            text-align: center;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        
        .feature-card:hover {{
            transform: translateY(-5px);
        }}
        
        .feature-icon {{
            font-size: 3em;
            margin-bottom: 20px;
            color: var(--primary-color);
        }}
        
        .feature-card h3 {{
            font-size: 1.5em;
            margin-bottom: 15px;
            color: var(--text-dark);
        }}
        
        /* Target Section */
        .target {{
            padding: 80px 0;
            background: var(--bg-light);
            text-align: center;
        }}
        
        .target-content {{
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .target h2 {{
            font-size: 2.5em;
            margin-bottom: 30px;
            color: var(--primary-color);
        }}
        
        .target p {{
            font-size: 1.2em;
            color: var(--text-light);
            margin-bottom: 40px;
        }}
        
        /* CTA Section */
        .cta-section {{
            background: var(--primary-color);
            color: white;
            padding: 80px 0;
            text-align: center;
        }}
        
        .cta-section h2 {{
            font-size: 2.5em;
            margin-bottom: 20px;
        }}
        
        .cta-section p {{
            font-size: 1.2em;
            margin-bottom: 40px;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2em;
            }}
            
            .features-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <h1>{product_info['product_name']}</h1>
            <p class="price">₩{product_info['price']:,}</p>
            <p class="description">{product_info.get('description', '혁신적인 제품으로 당신의 일상을 바꿔보세요')}</p>
            <a href="#" class="cta-button">지금 구매하기</a>
        </div>
    </section>
    
    <!-- Features Section -->
    <section class="features">
        <div class="container">
            <h2 class="section-title">주요 특징</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">✨</div>
                    <h3>뛰어난 품질</h3>
                    <p>엄선된 소재와 정교한 기술로 제작되어 오래도록 사용할 수 있습니다</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🚀</div>
                    <h3>혁신적 기능</h3>
                    <p>시장을 선도하는 최신 기술이 적용되어 편리한 사용 경험을 제공합니다</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">💎</div>
                    <h3>프리미엄 디자인</h3>
                    <p>{product_info.get('special_requirements', '세련되고 모던한 디자인')}으로 어디서나 돋보입니다</p>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Target Section -->
    <section class="target">
        <div class="container">
            <div class="target-content">
                <h2>이런 분들께 추천합니다</h2>
                <p>{product_info.get('target_market', '품질을 중시하는 스마트한 소비자')}</p>
                <a href="#" class="cta-button">자세히 알아보기</a>
            </div>
        </div>
    </section>
    
    <!-- CTA Section -->
    <section class="cta-section">
        <div class="container">
            <h2>지금 바로 시작하세요</h2>
            <p>특별 할인 혜택을 놓치지 마세요</p>
            <a href="#" class="cta-button" style="background: white; color: var(--primary-color);">구매하기</a>
        </div>
    </section>
</body>
</html>"""
    
    return html_content

# 메인 헤더
st.markdown("""
<div class="main-header">
    <h1>🚀 AI 상세페이지 생성기</h1>
    <p>몇 가지 정보만 입력하면 전문가 수준의 상세페이지가 완성됩니다!</p>
</div>
""", unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.title("🎯 사용 가이드")
    st.markdown("""
    ### 단 3단계로 완성!
    
    1. **정보 입력**: 제품 정보를 입력하세요
    2. **생성**: AI가 자동으로 페이지 생성
    3. **다운로드**: HTML 파일로 저장
    
    ---
    
    ### 💡 특징
    - 🎨 카테고리별 최적화 디자인
    - 📱 반응형 레이아웃
    - ⚡ 즉시 사용 가능한 HTML
    - 🔍 SEO 최적화
    """)
    
    # 예시 데이터 로드
    if st.button("📋 예시 데이터 사용"):
        st.session_state['example'] = True

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📝 정보 입력", "👁️ 미리보기", "📥 다운로드"])

with tab1:
    # 입력 모드 선택
    mode = st.radio(
        "입력 방식을 선택하세요",
        ["🎯 빠른 입력 (키워드만)", "📝 상세 입력 (전체 정보)"],
        horizontal=True
    )
    
    if mode == "🎯 빠른 입력 (키워드만)":
        keyword = st.text_input(
            "제품 키워드를 입력하세요",
            placeholder="예: AI 스마트 스피커, 프리미엄 무선 이어폰",
            value="AI 스마트 스피커 Pro" if st.session_state.get('example') else ""
        )
        
        if keyword:
            # 키워드에서 정보 추론
            if "이어폰" in keyword or "헤드폰" in keyword:
                category = "전자제품"
                price = 199000
            elif "옷" in keyword or "패션" in keyword:
                category = "패션"
                price = 89000
            elif "화장품" in keyword or "스킨" in keyword:
                category = "뷰티"
                price = 59000
            elif "책" in keyword or "도서" in keyword:
                category = "경영경제서적"
                price = 20000
            else:
                category = "기타"
                price = 99000
            
            if "프리미엄" in keyword or "럭셔리" in keyword:
                price = int(price * 1.5)
            
            product_info = {
                "product_name": keyword,
                "category": category,
                "price": price,
                "description": f"최고의 품질과 디자인을 자랑하는 {keyword}",
                "target_market": "품질을 중시하는 스마트 컨슈머",
                "special_requirements": "트렌디하고 세련된 디자인"
            }
    
    else:  # 상세 입력 모드
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.text_input(
                "제품명 *",
                placeholder="예: AI 스마트 워치",
                value="경영컨설팅은 끝났다" if st.session_state.get('example') else ""
            )
            
            category = st.selectbox(
                "카테고리 *",
                ["전자제품", "패션", "뷰티", "경영경제서적", "식품", "기타"],
                index=3 if st.session_state.get('example') else 0
            )
            
            price = st.number_input(
                "가격 (원) *",
                min_value=0,
                value=20000 if st.session_state.get('example') else 99000,
                step=1000
            )
        
        with col2:
            target_market = st.text_input(
                "타겟 고객",
                placeholder="예: 30-40대 직장인",
                value="예비창업자, 초기 중소상공인 사업자, 컨설턴트" if st.session_state.get('example') else ""
            )
            
            special_requirements = st.text_area(
                "디자인 요구사항",
                placeholder="미니멀한 디자인, 신뢰감 있는 느낌",
                value="세련되고 미니멀하게, 도시적이고 진취적" if st.session_state.get('example') else ""
            )
            
            brand_color = st.color_picker(
                "브랜드 색상",
                "#2C3E50" if st.session_state.get('example') else "#1a73e8"
            )
        
        description = st.text_area(
            "제품 설명",
            placeholder="제품의 주요 특징과 장점을 설명해주세요",
            value="기존의 방식을 고집하면 안된다. 새로운 시대 AI를 잘 활용하여 생산성과 능률을 올려서 위기를 기회로 만들자" if st.session_state.get('example') else ""
        )
        
        if product_name:
            product_info = {
                "product_name": product_name,
                "category": category,
                "price": price,
                "description": description,
                "target_market": target_market,
                "special_requirements": special_requirements,
                "brand_color": brand_color
            }
    
    # 생성 버튼
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("✨ 상세페이지 생성", type="primary", use_container_width=True):
            if mode == "🎯 빠른 입력 (키워드만)" and keyword:
                with st.spinner("AI가 상세페이지를 생성하고 있습니다..."):
                    html_content = generate_detail_page(product_info)
                    st.session_state['generated_html'] = html_content
                    st.session_state['product_info'] = product_info
                    st.success("✅ 상세페이지가 생성되었습니다!")
                    st.info("👉 '미리보기' 탭에서 결과를 확인하세요!")
                    
            elif mode == "📝 상세 입력 (전체 정보)" and product_name:
                with st.spinner("AI가 상세페이지를 생성하고 있습니다..."):
                    html_content = generate_detail_page(product_info)
                    st.session_state['generated_html'] = html_content
                    st.session_state['product_info'] = product_info
                    st.success("✅ 상세페이지가 생성되었습니다!")
                    st.info("👉 '미리보기' 탭에서 결과를 확인하세요!")
                    
            else:
                st.error("필수 정보를 입력해주세요!")

with tab2:
    if 'generated_html' in st.session_state:
        st.subheader("🎨 생성된 상세페이지 미리보기")
        
        # 디바이스 선택
        device = st.radio(
            "미리보기 디바이스",
            ["💻 데스크톱", "📱 모바일"],
            horizontal=True
        )
        
        if device == "💻 데스크톱":
            st.components.v1.html(st.session_state['generated_html'], height=800, scrolling=True)
        else:
            # 모바일 미리보기
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("""
                <div style="max-width:375px;margin:0 auto;border:10px solid #333;border-radius:20px;overflow:hidden;">
                </div>
                """, unsafe_allow_html=True)
                st.components.v1.html(
                    st.session_state['generated_html'],
                    height=667,
                    scrolling=True
                )
    else:
        st.info("📝 먼저 정보를 입력하고 상세페이지를 생성해주세요.")

with tab3:
    if 'generated_html' in st.session_state:
        st.subheader("📥 생성된 파일 다운로드")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📄 HTML 파일")
            html_download = st.download_button(
                label="📥 HTML 다운로드",
                data=st.session_state['generated_html'],
                file_name=f"{st.session_state['product_info']['product_name']}_상세페이지.html",
                mime="text/html",
                use_container_width=True
            )
            
        with col2:
            st.markdown("### 📊 프로젝트 정보")
            project_info = {
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "product_info": st.session_state['product_info'],
                "template": "AI Generated"
            }
            
            json_download = st.download_button(
                label="📥 프로젝트 정보 (JSON)",
                data=json.dumps(project_info, ensure_ascii=False, indent=2),
                file_name=f"{st.session_state['product_info']['product_name']}_info.json",
                mime="application/json",
                use_container_width=True
            )
        
        # 사용 가이드
        st.markdown("---")
        st.markdown("### 📌 사용 방법")
        st.markdown("""
        1. **HTML 파일 다운로드**: 생성된 상세페이지를 다운로드합니다
        2. **웹 서버에 업로드**: 다운로드한 HTML 파일을 웹 서버에 업로드합니다
        3. **커스터마이징**: 필요에 따라 HTML/CSS를 수정합니다
        """)
        
        # 코드 미리보기
        with st.expander("🔍 HTML 코드 미리보기"):
            st.code(st.session_state['generated_html'][:1000] + "...", language="html")
    else:
        st.info("📝 먼저 정보를 입력하고 상세페이지를 생성해주세요.")

# 푸터
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p>Made with ❤️ by AI Detail Page Generator</p>
    <p>Powered by Streamlit & Claude</p>
    </div>
    """,
    unsafe_allow_html=True
)