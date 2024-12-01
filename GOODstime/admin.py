from django.contrib import admin
from .models import Admin_user, Post,Comment, Message, Review, Report, Favorite, Block, Stripe_Customer
from django.utils.safestring import mark_safe

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'work_name',
        'content',
        'tag1',
        'tag2',
        'tag3',
        'give_character',
        'want_character',
        'price',
        'type_transaction',
        'type_transfer',
        'match_user',
        'status',
        'thumbnail_image1',
        'thumbnail_image2',
        'thumbnail_image3',
        'delete_flg',
        'created_at',
        'updated_at',
    )
    search_fields = ('user', 'work_name', 'give_character', 'tag1','status',)

    # サムネイル画像1
    def thumbnail_image1(self, obj):
        if obj.image1:  # image1が存在する場合
            return mark_safe(f'<img src="{obj.image1.url}" style="width:100px; height:auto;">')
        return "No Image"

    thumbnail_image1.short_description = 'Image 1'

    # サムネイル画像2
    def thumbnail_image2(self, obj):
        if obj.image2:  # image2が存在する場合
            return mark_safe(f'<img src="{obj.image2.url}" style="width:100px; height:auto;">')
        return "No Image"

    thumbnail_image2.short_description = 'Image 2'

    # サムネイル画像3
    def thumbnail_image3(self, obj):
        if obj.image3:  # image3が存在する場合
            return mark_safe(f'<img src="{obj.image3.url}" style="width:100px; height:auto;">')
        return "No Image"

    thumbnail_image3.short_description = 'Image 3'

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'post',
        'content',
        'created_at',
    )
    search_fields = ('user', 'post', )

class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'post',
        'content',
        'created_at',
    )
    search_fields = ('user', 'post', )

class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'post',
        'target_user',
        'score',
        'comment',
        'created_at',
    )
    search_fields = ('user', 'target_user', )

class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'post',
        'created_at',
        'updated_at',
    )
    search_fields = ('user', )

class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'post',
        'comment',
        'created_at',
        'updated_at',
    )
    search_fields = ('user',)

class BlockAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'target_user',
        'created_at',
        'updated_at',
    )
    search_fields = ('user', 'target_user', )

class Stripe_CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'stripeCustomerId', 'stripeSubscriptionId', 'stripePaymentMethodId', 'created_at', 'updated_at')
    search_fields = ('user', )

class Admin_userAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_date', 'updated_date')
    search_fields = ('name', )

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Favorite,FavoriteAdmin)
admin.site.register(Report,ReportAdmin)
admin.site.register(Block,BlockAdmin)
admin.site.register(Stripe_Customer, Stripe_CustomerAdmin)
admin.site.register(Admin_user, Admin_userAdmin)