import streamlit as st
import requests

st.set_page_config(page_title="Business Plan Creator", page_icon="📊")

st.title("Business Plan Creator")
st.write("Generate a comprehensive business plan using AI")

# Input field for business concept
business_concept = st.text_input("Describe your business concept in 1-2 sentences:", placeholder="e.g., A sustainable fashion brand using recycled materials")

if st.button("Generate Business Plan"):
    if business_concept:
        with st.spinner("Generating your business plan..."):
            try:
                # Call the FastAPI backend
                response = requests.post(
                    "http://localhost:8000/generate-business-plan",
                    json={"business_concept": business_concept}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display each agent's response
                    st.markdown("### Generated Business Plan")
                    
                    # Combine all responses for the download
                    full_content = "# Business Plan\n\n"
                    
                    for agent_response in result["responses"]:
                        st.markdown(f"#### {agent_response['role']}")
                        st.markdown(agent_response['content'])
                        st.markdown("---")
                        
                        # Add to full content for download
                        full_content += f"## {agent_response['role']}\n\n"
                        full_content += agent_response['content']
                        full_content += "\n\n---\n\n"
                    
                    # Add download button with full content
                    st.download_button(
                        label="Download Business Plan",
                        data=full_content,
                        file_name="business_plan.md",
                        mime="text/markdown"
                    )
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Error connecting to the server: {str(e)}")
    else:
        st.warning("Please describe your business concept.") 