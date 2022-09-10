from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = "authors"
        
    def __str__(self):
        return f"[작가] id: {self.id} / 닉네임: {self.user.nickname}"


class Exhibition(models.Model):
    title = models.CharField("제목", max_length=64)
    start_date = models.DateTimeField("시작일")
    end_date = models.DateTimeField("종료일")
    
    class Meta:
        db_table = "exhibitions"
        
    def __str__(self):
        return f"[전시] id: {self.id} / 제목: {self.title}"


class Art(models.Model):
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    title = models.CharField("제목", max_length=64)
    price = models.PositiveIntegerField("가격")
    size = models.PositiveIntegerField("호수", validators=[MinValueValidator(1), MaxValueValidator(500)])
    created_at = models.DateTimeField("등록일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)
    exhibition = models.ForeignKey(Exhibition, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = "arts"
    
    def __str__(self):
        return f"[작품] id: {self.id} / 제목: {self.title}"
    
    