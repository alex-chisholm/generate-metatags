import streamlit as st

st.set_page_config(
    page_title="Social Media Meta Tags Generator",
    page_icon="🔖",
    menu_items={
        'About': "Generate appropriate social media meta tags for different web frameworks"
    }
)

def generate_streamlit_code(title, description, url, image_url):
    code = f"""
st.set_page_config(
    page_title="{title}",
    page_icon="🔖",
    menu_items={{
        'About': "{description}"
    }}
)    
    """
    if image_url:
        code += f'\n# Note: Streamlit currently does not support custom social media preview images directly'
    return code

def generate_dash_code(title, description, url, image_url):
    code = f"""
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{title}</title>
        <meta property="og:title" content="{title}" />
        <meta property="og:description" content="{description}" />'''"""
    
    if url:
        code += f'\n        <meta property="og:url" content="{url}" />'
    if image_url:
        code += f'\n        <meta property="og:image" content="{image_url}" />'
    
    code += """
        {{%css%}}
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
'''"""
    return code

def generate_shiny_python_code(title, description, url, image_url):
    code = f"""
app.title = "{title}"

@app.server.hook('before_first_request')
def add_meta_tags():
    meta_tags = [
        {{'property': 'og:title', 'content': '{title}'}},
        {{'property': 'og:description', 'content': '{description}'}}"""
    
    if url:
        code += f",\n        {{'property': 'og:url', 'content': '{url}'}}"
    if image_url:
        code += f",\n        {{'property': 'og:image', 'content': '{image_url}'}}"
    
    code += """
    ]
    app.server.meta_tags.extend(meta_tags)
"""
    return code

def generate_shiny_r_code(title, description, url, image_url):
    code = f"""
add_meta <- function() {{
  tags$head(
    tags$title("{title}"),
    tags$meta(property = "og:title", content = "{title}"),
    tags$meta(property = "og:description", content = "{description}")"""
    
    if url:
        code += f',\n    tags$meta(property = "og:url", content = "{url}")'
    if image_url:
        code += f',\n    tags$meta(property = "og:image", content = "{image_url}")'
    
    code += """
  )
}

ui <- fluidPage(
  add_meta(),
  # Your UI components here
)
"""
    return code

def generate_quarto_code(title, description, url, image_url):
    code = """---"""
    if title:
        code += f'\ntitle: "{title}"'
    if description:
        code += f'\ndescription: "{description}"'
    
    code += "\nformat:\n  html:\n    metadata:"
    if url:
        code += f'\n      og:url: "{url}"'
    if image_url:
        code += f'\n      og:image: "{image_url}"'
    
    code += "\n---"
    return code

def main():
    st.title("Social Media Meta Tags Generator")
    st.write("Generate appropriate social media meta tags for different web frameworks")
    
    title = st.text_input("Title", placeholder="Enter your page title")
    description = st.text_area("Description", placeholder="Enter your page description")
    url = st.text_input("URL", placeholder="Enter your page URL (optional)")
    image_url = st.text_input("Image URL", placeholder="Enter your preview image URL (optional)")
    
    framework = st.selectbox(
        "Select your framework",
        ["Streamlit", "Dash", "Shiny for Python", "Shiny for R", "Quarto"]
    )
    
    if st.button("Generate Code"):
        if not title or not description:
            st.error("Title and Description are required!")
            return
            
        st.subheader("Generated Code")
        
        code = None
        if framework == "Streamlit":
            code = generate_streamlit_code(title, description, url, image_url)
        elif framework == "Dash":
            code = generate_dash_code(title, description, url, image_url)
        elif framework == "Shiny for Python":
            code = generate_shiny_python_code(title, description, url, image_url)
        elif framework == "Shiny for R":
            code = generate_shiny_r_code(title, description, url, image_url)
        elif framework == "Quarto":
            code = generate_quarto_code(title, description, url, image_url)
            
        st.code(code, language='python' if framework != "Shiny for R" else 'r')
        
        if framework == "Streamlit":
            st.info("Note: Streamlit currently has limited support for custom social media preview metadata. The generated code provides basic page configuration.")

if __name__ == "__main__":
    main()
