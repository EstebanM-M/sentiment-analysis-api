"""
Streamlit Demo App for Sentiment Analysis API
Run with: streamlit run app_demo.py
"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time
import sys
import os

# Add src to path for local imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import local modules
from models.sentiment_model import SentimentAnalyzer
from database.database import SessionLocal, init_db
from database import crud


# Page config
st.set_page_config(
    page_title="Sentiment Analysis API - Demo",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .positive {
        color: #28a745;
        font-weight: bold;
    }
    .negative {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Load the sentiment analysis model (cached)"""
    with st.spinner("🤖 Loading AI model... (first time only)"):
        analyzer = SentimentAnalyzer()
    return analyzer


@st.cache_resource
def get_db():
    """Initialize database"""
    init_db()
    return SessionLocal()


def main():
    # Header
    st.markdown('<h1 class="main-header">🎭 Sentiment Analysis API</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align: center; font-size: 1.2rem; color: #666;">Powered by DistilBERT | '
        'Built with FastAPI & Streamlit</p>',
        unsafe_allow_html=True
    )
    
    # Load model
    try:
        analyzer = load_model()
        db = get_db()
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        st.stop()
    
    # Sidebar
    st.sidebar.header("📊 About")
    st.sidebar.info(
        """
        **Sentiment Analysis API**
        
        This is a production-ready API that analyzes 
        the sentiment of text using a pre-trained 
        DistilBERT model.
        
        **Features:**
        - Real-time sentiment analysis
        - Batch processing
        - Historical data storage
        - RESTful API endpoints
        - Statistics & analytics
        
        **Tech Stack:**
        - FastAPI
        - Transformers (DistilBERT)
        - PostgreSQL
        - SQLAlchemy
        - Streamlit (this demo)
        """
    )
    
    # Model info
    st.sidebar.header("🤖 Model Info")
    st.sidebar.markdown(f"""
    - **Model:** {analyzer.model_name}
    - **Device:** {'GPU' if analyzer.device == 0 else 'CPU'}
    - **Accuracy:** ~95%
    """)
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Single Analysis", 
        "📦 Batch Analysis", 
        "📊 Statistics",
        "🔍 History"
    ])
    
    # ==================== TAB 1: SINGLE ANALYSIS ====================
    with tab1:
        st.header("Analyze Text Sentiment")
        
        # Example texts
        examples = {
            "Select an example...": "",
            "Positive Review": "This product is absolutely amazing! Best purchase I've ever made.",
            "Negative Review": "Terrible experience. Would not recommend to anyone.",
            "Neutral Statement": "The package arrived on time as expected.",
            "Mixed Sentiment": "The food was great but the service was disappointing.",
        }
        
        col1, col2 = st.columns([3, 1])
        with col1:
            example_choice = st.selectbox("Try an example:", list(examples.keys()))
        
        # Text input
        default_text = examples[example_choice] if example_choice != "Select an example..." else ""
        text_input = st.text_area(
            "Enter text to analyze:",
            value=default_text,
            height=100,
            placeholder="Type or paste your text here..."
        )
        
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
        with col2:
            save_result = st.checkbox("Save to database", value=True)
        
        if analyze_button and text_input:
            with st.spinner("Analyzing..."):
                start_time = time.time()
                
                try:
                    # Analyze
                    result = analyzer.analyze(text_input)
                    processing_time = (time.time() - start_time) * 1000
                    
                    # Display result
                    st.success("✅ Analysis Complete!")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        sentiment = result['label']
                        color = "positive" if sentiment == "POSITIVE" else "negative"
                        st.markdown(f'<div class="metric-card"><h3>Sentiment</h3>'
                                  f'<p class="{color}" style="font-size: 2rem;">{sentiment}</p></div>',
                                  unsafe_allow_html=True)
                    
                    with col2:
                        score = result['score']
                        st.markdown(f'<div class="metric-card"><h3>Confidence</h3>'
                                  f'<p style="font-size: 2rem;">{score:.2%}</p></div>',
                                  unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f'<div class="metric-card"><h3>Processing Time</h3>'
                                  f'<p style="font-size: 2rem;">{processing_time:.0f}ms</p></div>',
                                  unsafe_allow_html=True)
                    
                    # Progress bar for confidence
                    st.progress(score)
                    
                    # Save to database
                    if save_result:
                        try:
                            crud.create_analysis(
                                db=db,
                                text=text_input,
                                label=sentiment,
                                score=score,
                                processing_time_ms=processing_time,
                                model_name=analyzer.model_name,
                                is_batch=False
                            )
                            st.info("💾 Result saved to database")
                        except Exception as e:
                            st.warning(f"⚠️ Could not save to database: {str(e)}")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # ==================== TAB 2: BATCH ANALYSIS ====================
    with tab2:
        st.header("Batch Analysis")
        st.markdown("Analyze multiple texts at once")
        
        # Text input
        batch_input = st.text_area(
            "Enter texts (one per line):",
            height=200,
            placeholder="Line 1: First text to analyze\nLine 2: Second text to analyze\nLine 3: Third text to analyze"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            batch_button = st.button("🚀 Analyze Batch", type="primary", use_container_width=True)
        
        if batch_button and batch_input:
            texts = [line.strip() for line in batch_input.split('\n') if line.strip()]
            
            if not texts:
                st.warning("⚠️ Please enter at least one text")
            else:
                with st.spinner(f"Analyzing {len(texts)} texts..."):
                    start_time = time.time()
                    
                    try:
                        # Analyze batch
                        results = analyzer.analyze_batch(texts)
                        total_time = (time.time() - start_time) * 1000
                        
                        st.success(f"✅ Analyzed {len(results)} texts in {total_time:.0f}ms")
                        
                        # Summary metrics
                        positive_count = sum(1 for r in results if r['label'] == 'POSITIVE')
                        negative_count = len(results) - positive_count
                        avg_score = sum(r['score'] for r in results) / len(results)
                        
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Total", len(results))
                        col2.metric("Positive", positive_count, delta=f"{positive_count/len(results)*100:.0f}%")
                        col3.metric("Negative", negative_count, delta=f"{negative_count/len(results)*100:.0f}%")
                        col4.metric("Avg Confidence", f"{avg_score:.2%}")
                        
                        # Results table
                        st.subheader("Results")
                        df = pd.DataFrame(results)
                        df['score'] = df['score'].apply(lambda x: f"{x:.2%}")
                        
                        # Color code by sentiment
                        def highlight_sentiment(row):
                            if row['label'] == 'POSITIVE':
                                return ['background-color: #d4edda'] * len(row)
                            else:
                                return ['background-color: #f8d7da'] * len(row)
                        
                        st.dataframe(
                            df.style.apply(highlight_sentiment, axis=1),
                            use_container_width=True,
                            hide_index=True
                        )
                        
                        # Save to database
                        try:
                            for text, result in zip(texts, results):
                                crud.create_analysis(
                                    db=db,
                                    text=text,
                                    label=result['label'],
                                    score=result['score'],
                                    processing_time_ms=total_time / len(results),
                                    model_name=analyzer.model_name,
                                    is_batch=True
                                )
                            st.info("💾 All results saved to database")
                        except Exception as e:
                            st.warning(f"⚠️ Could not save to database: {str(e)}")
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # ==================== TAB 3: STATISTICS ====================
    with tab3:
        st.header("📊 Analysis Statistics")
        
        try:
            stats = crud.get_statistics(db)
            
            if stats['total_analyses'] == 0:
                st.info("📊 No analyses yet. Try analyzing some texts first!")
            else:
                # Overview metrics
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Analyses", stats['total_analyses'])
                col2.metric("Positive", stats['positive_count'], 
                          delta=f"{stats['positive_percentage']:.1f}%")
                col3.metric("Negative", stats['negative_count'],
                          delta=f"{stats['negative_percentage']:.1f}%")
                col4.metric("Avg Confidence", f"{stats['average_score']:.2%}")
                
                # Charts
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Sentiment Distribution")
                    sentiment_data = pd.DataFrame({
                        'Sentiment': ['Positive', 'Negative'],
                        'Count': [stats['positive_count'], stats['negative_count']]
                    })
                    st.bar_chart(sentiment_data.set_index('Sentiment'))
                
                with col2:
                    st.subheader("Performance")
                    st.metric("Avg Processing Time", f"{stats['average_processing_time']:.0f}ms")
                    st.metric("Total Batch Analyses", stats.get('batch_count', 0))
                
                # Recent activity
                st.subheader("📅 Recent Activity")
                recent = crud.get_recent_analyses(db, limit=10)
                
                if recent:
                    recent_df = pd.DataFrame([{
                        'Text': r.text[:50] + '...' if len(r.text) > 50 else r.text,
                        'Sentiment': r.label,
                        'Confidence': f"{r.score:.2%}",
                        'Time': r.created_at.strftime('%Y-%m-%d %H:%M')
                    } for r in recent])
                    
                    st.dataframe(recent_df, use_container_width=True, hide_index=True)
        
        except Exception as e:
            st.error(f"❌ Error loading statistics: {str(e)}")
    
    # ==================== TAB 4: HISTORY ====================
    with tab4:
        st.header("🔍 Analysis History")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_sentiment = st.selectbox("Filter by sentiment:", ["All", "POSITIVE", "NEGATIVE"])
        with col2:
            filter_limit = st.slider("Show last N records:", 10, 100, 50)
        with col3:
            search_term = st.text_input("Search text:")
        
        try:
            # Get history
            if search_term:
                history = crud.search_analyses(db, search_term, limit=filter_limit)
            else:
                label_filter = None if filter_sentiment == "All" else filter_sentiment
                history = crud.get_analyses(db, label=label_filter, limit=filter_limit)
            
            if not history:
                st.info("📭 No results found")
            else:
                st.success(f"Found {len(history)} results")
                
                # Display as dataframe
                history_df = pd.DataFrame([{
                    'ID': h.id,
                    'Text': h.text[:80] + '...' if len(h.text) > 80 else h.text,
                    'Sentiment': h.label,
                    'Confidence': f"{h.score:.2%}",
                    'Batch': '✓' if h.is_batch else '✗',
                    'Time': h.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'Processing (ms)': f"{h.processing_time_ms:.0f}"
                } for h in history])
                
                st.dataframe(history_df, use_container_width=True, hide_index=True)
                
                # Export option
                csv = history_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"sentiment_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        except Exception as e:
            st.error(f"❌ Error loading history: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666;">Built by Esteban | '
        '<a href="https://github.com/EstebanM-M/sentiment-analysis-api">GitHub</a> | '
        'FastAPI + Transformers + Streamlit</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
