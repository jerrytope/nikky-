from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('get_total_price',)
    fields = ('product', 'price', 'quantity', 'get_total_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'total_amount', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at', 'updated_at')
    search_fields = ('id', 'user__email', 'first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'user', 'total_amount', 'status', 'payment_status', 'payment_reference')
        }),
        ('Customer Information', {
            'fields': ('email', 'first_name', 'last_name', 'phone')
        }),
        ('Shipping Information', {
            'fields': ('address', 'city', 'state', 'postal_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Customer Name'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'quantity', 'get_total_price')
    list_filter = ('order__status', 'order__payment_status')
    search_fields = ('order__id', 'product__name')
    ordering = ('-order__created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'product')
