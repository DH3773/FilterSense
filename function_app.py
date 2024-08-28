import azure.functions as func
import logging
from filter_services import apply_filter_to_image

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="apply_filter")
def apply_filter(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get the filter from the query string or request body
    filter = req.params.get('filter')
    if not filter:
        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse(
                "Please select a filter",
                status_code=400
            )
        else:
            filter = req_body.get('filter')

    # Get the image from the request or return an error if not found
    image_file = req.files.get('image')
    if not image_file:
        return func.HttpResponse(
            "Please upload an image",
            status_code=400
        )
    
    # Read the image data from the file pointer
    image_data = image_file.read()

    # Apply the filter to the image
    filtered_image_data = apply_filter_to_image(image_data, filter)

    # Return the filtered image
    return func.HttpResponse(
        filtered_image_data,
        status_code=200,
        mimetype='image/jpeg' # Make sure to set the correct MIME type
    )





@app.route(route="default")
def default(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )