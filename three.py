import streamlit as st
import firebase_admin
from firebase_admin import credentials, db, storage
import tempfile

# Initialize Firebase Admin SDK if it hasn't been initialized yet
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate('images-cf8c0-firebase-adminsdk-r2rm3-a2e9632835.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://images-cf8c0-default-rtdb.firebaseio.com/',
        'storageBucket': 'images-cf8c0.appspot.com'
    })

# Function to store product data in Firebase
def store_product(product):
    ref = db.reference('products')  # Reference to the 'products' node in your Firebase database
    ref.push(product)  # Push the product data to Firebase

# Function to upload images to Firebase Storage
def upload_image(image_file, path):
    bucket = storage.bucket()
    blob = bucket.blob(path)
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(image_file.read())
        blob.upload_from_filename(temp.name)
    return blob.public_url

# Streamlit app
def main():
    st.title('Product Details Input')

    # Input fields for product details
    product_code = st.text_input('Product Code', 'Diary001')
    product_name = st.text_input('Product Name', 'The Floral Art Notebook')
    sku = st.text_input('SKU', '99S_NB_001')
    product_category = st.text_input('Product Category', 'Diary')
    sub_category = st.text_input('Sub Category', 'Line Art')
    description = st.text_area('Description', 'Let your thoughts bloom with our stunning diary adorned with minimalistic floral art.')
    specification = st.text_area('Specification', 'Specifications:\nSize: A5 | Hardbound | 80 Pages (Ruled)\nPrice: 399/- only | Free Shipping in India')
    price = st.number_input('Price', value=399)
    gst = st.selectbox('GST', ['Inclusive', 'Exclusive'])

    # File uploaders for images
    front_image = st.file_uploader("Upload Front Image", type=['jpg', 'jpeg', 'png'])
    back_image = st.file_uploader("Upload Back Image", type=['jpg', 'jpeg', 'png'])
    inner_cover_image = st.file_uploader("Upload Inner Cover Image", type=['jpg', 'jpeg', 'png'])
    inner_page_image = st.file_uploader("Upload Inner Page Image", type=['jpg', 'jpeg', 'png'])

    if st.button('Submit'):
        product = {
            'productCode': product_code,
            'productName': product_name,
            'sku': sku,
            'productCategory': product_category,
            'subCategory': sub_category,
            'description': description,
            'specification': specification,
            'price': price,
            'gst': gst,
        }

        # Upload images and add URLs to the product dictionary
        if front_image:
            product['frontImageUrl'] = upload_image(front_image, f"images/{product_code}/front.jpg")
        if back_image:
            product['backImageUrl'] = upload_image(back_image, f"images/{product_code}/back.jpg")
        if inner_cover_image:
            product['innerCoverImageUrl'] = upload_image(inner_cover_image, f"images/{product_code}/inner_cover.jpg")
        if inner_page_image:
            product['innerPageImageUrl'] = upload_image(inner_page_image, f"images/{product_code}/inner_page.jpg")
            

        store_product(product)
        st.success('Product details successfully submitted to Firebase!')

if __name__ == '__main__':
    main()
