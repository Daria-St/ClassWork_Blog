from rest_framework import serializers
from core.models import PostComment, Feedback, Post


class CommentsSerialaizer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True) # если захотели передать id, read_only=True - поля, которые не участвуют в записи
    text = serializers.CharField(max_length=10) #CharField - тип поля, кот лежит в ser, max_length - ограничение количества символов
    my_field = serializers.SerializerMethodField(read_only=True)
    profile = serializers.SerializerMethodField()

    #чтобы дать значение кастомному полю - надо прописать метод
    def get_my_field(self, obj):
        return 42

    def get_profile(self, obj):
        return obj.profile.user.username

    def create(self, validated_data):
        '''Создаем объект комментария в базе '''
        # PostComment.objects.create(**validated_data)  - тоже самое, что 4 строки ниже
        text = validated_data['text']
        profile = validated_data['profile']
        post = validated_data['post']
        return PostComment.objects.create(text=text, post=post, profile=profile)


class FeedbackSerialaizer(serializers.Serializer):
    name = serializers.CharField()
    text = serializers.CharField()

    def create(self, validated_data):
        return Feedback.objects.create(**validated_data)


    #модельная форма сериалайзера
class PostSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__' # если хотим загрузить все поля
        # fields = ['title'] # если хотим загрузить конкретное поле


