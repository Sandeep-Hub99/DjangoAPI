from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import Article, Passenger

#Serialization_Classes

# class ArticleSerializer(serializers.Serializer):
#     title       = serializers.CharField(max_length=100)
#     description = serializers.CharField(max_length=400)


#     def create(self, validated_data):
#         return Article.objects.create(validated_data)

#     def update(self, instance, validated_data):
#         instance.title       = validated_data.get('title',instance.title)
#         instance.description = validated_data.get('description',instance.description)

#ModelSerilizer_Classes
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id','title','description']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    mobile = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        mobile = data.get("mobile")
        password = data.get("password")

        if not mobile and password:
            raise ValidationError("Username and Password is required")
        try:
            passenger = Passenger.objects.get(mobile=mobile)
        except Passenger.DoesNotExist:
            raise ValidationError("This email address does not exist")
        if passenger.password == password:
            data["passenger_id"] = passenger.id
            return data
        else:
            raise ValidationError("Invalid credentials")