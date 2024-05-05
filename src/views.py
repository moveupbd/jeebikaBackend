from django.http import HttpResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter

from employees.models import job_post
from employees.serializers import PrivateEmployeePostSerializer

from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404



def hello_world(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Active Server</title>
        <style>
            body {
                font-family: "Lucida Console", "Courier New", monospace;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color:black;
            }
            .message {
                text-align: center;
                color:white;
                padding-bottom:30px;
                font-size:28px;
            }
            .image{
                height:200px;
                weight:200px;
                overflow:hidden;
                padding-left:32px;
            }
            img{
                border-radius:100px;
                height:200px;
                weight:200px;
                object-fit:fill;
            }
            .company{
                text-align:center;
                color:white;
                font-size:24px;
            }
        </style>
    </head>
    <body>
        <div class="content">
            <div class="message">
                Jeebika Backend!
            </div>
            <div class="image">
                <img src="https://thumbs.dreamstime.com/z/backend-developer-line-icon-linear-style-sign-mobile-concept-web-design-person-working-database-server-outline-vector-310897949.jpg?w=768">
            </div>
            <div class="company">
                <h5>moveupbangladesh.com</h5>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)


class PublicEmployeeposts(ListAPIView):
    serializer_class = PrivateEmployeePostSerializer
    permission_classes = []
    filter_backends = [SearchFilter]
    search_fields = ["category__name"]
    queryset = job_post.objects.all().order_by('-id')
    
    
class PublicEmployeePostDetail(RetrieveAPIView):
    serializer_class = PrivateEmployeePostSerializer

    def get_object(self):
        uid = self.kwargs.get("post_uid")
        if uid is None:
            # Handle the case where `post_uid` is not provided in the URL
            raise ValidationError("Post UID is required.")

        # Filter job_post queryset by UID
        return get_object_or_404(job_post, uid=uid)