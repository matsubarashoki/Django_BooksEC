from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.dispatch import receiver
from base.models import create_id


class UserManager(BaseUserManager):
    """BaseUserManagerクラスはユーザーを生成する時使うヘルパー(Helper)クラス
        実際のモデル(Model)はAbstractBaseUserを継承して作るクラスです。
    """
    #通常ユーザ作成メソッドをオーバーライド
    def create_user(self, username, email, password=None):
        #メールのバリデーション
        if not email:
            raise ValueError("メアドは必須なり")
        #ユーザオブジェクト作成
        user = self.model(
            username = username,
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username,
            email,
            password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.CharField(default=create_id, primary_key=True, editable=False, max_length=22)
    username = models.CharField(max_length=50, unique=True,blank=True, default='匿名')
    email = models.EmailField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    object = UserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email,']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None): #permission判定用メソッド
        "Does the user have a specific permission?"
        return True
    
    def has_module_perms(self, app_label): 
        "Does the user have permissions to view the app 'app_label' ? "
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

class Profile(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE
    )
    name = models.CharField(default='', blank=True, max_length=50)
    zipcode = models.CharField(default='',blank=True,max_length=8)
    prefecture = models.CharField(default='',blank=True,max_length=50)
    city = models.CharField(default='',blank=True,max_length=50)
    address1 = models.CharField(default='',blank=True,max_length=50)
    address2 = models.CharField(default='',blank=True,max_length=50)
    tel = models.CharField(default='',blank=True,max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# OneToOneFiledを同時に作成　
# デコレーターreceiver　引数内の関数が呼ばれる直後に実行する関数にする
@receiver(post_save, sender=User)
def create_onetoone(sender, **kwargs):
    if kwargs['created']:#UserModelが作成されたかのフラグで判定
        Profile.objects.create(user=kwargs['insance'])