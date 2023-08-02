from flask import Blueprint, render_template, flash, redirect, url_for, request, session, jsonify
from app import db
from app.forms import EditProductsForm, OrderForm
from app.models import ProductsList, ShoppingCart, OrderList, OrderItem
from flask_login import login_required, current_user

products_bp = Blueprint('products', __name__)

# 商品列表路由
@products_bp.route('/')
def products():
    form = OrderForm()
    products_list = ProductsList.query.all()
    return render_template('products/products.html', products_list=products_list, form=form)

# 編輯商品（管理者功能）路由
@login_required
@products_bp.route('/edit', methods=['GET', 'POST'])
def edit_products():
    if not current_user.is_admin:
        flash('驗證失敗', category='error')
        return redirect(url_for('products.products'))
    
    form = EditProductsForm()
    if request.method == 'POST':
        product_name  = form.product_name.data
        product_price = form.product_price.data
        
        if form.submit_add.data:  # 如果是「新增商品」的提交
            if form.validate_on_submit():
                product = ProductsList(product_name=product_name, product_price=product_price)
                db.session.add(product)
                db.session.commit()
                flash('新增成功', category='success')
                return redirect(url_for('products.products'))
        elif form.submit_remove.data:  # 如果是「移除商品」的提交
            existing_product = ProductsList.query.filter_by(product_name=product_name).first()
            
            if existing_product:
                db.session.delete(existing_product)
                db.session.commit()
                flash('移除成功', category='success')
                return redirect(url_for('products.products'))
            else:
                flash('商品不存在', category='error')

    return render_template('products/edit_products.html', form=form)

# 將商品新增到購物車路由
@login_required
@products_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():

    product_ids = request.form.getlist('product_ids[]')
    quantities = request.form.getlist('quantities[]')
    quantities = [int(quantity) for quantity in quantities if quantity]

    if not all(quantity >= 0 for quantity in quantities):
        flash('商品數量不合法', category='error')
        return redirect(url_for('products.products'))

    if all(quantity == 0 for quantity in quantities):
        flash('您尚未選擇商品', category='error')
        return redirect(url_for('products.products'))

    for product_id, quantity in zip(product_ids, quantities):
        if quantity > 0:  # 只處理數量大於0的商品
            product = ProductsList.query.get(product_id)
            if product:
                order_list = ShoppingCart(
                    product_name=product.product_name,
                    product_price=product.product_price,
                    quantity=quantity,
                    user_id=current_user.id
                )
                db.session.add(order_list)
            else:
                flash('商品不存在', category='error')
                return redirect(url_for('products.products'))

    db.session.commit()  # 將購物車中所有有效的商品一次性新增進資料庫

    flash('成功加入購物車')
    return redirect(url_for('products.products'))

# 查看購物車路由
@login_required
@products_bp.route('/view_cart', methods=['GET','POST'])
def view_cart():

    car_list = ShoppingCart.query.filter_by(user_id=current_user.id).all()

    # 計算購物車中商品的總價（total）
    total = int(sum(item.product_price * item.quantity for item in car_list))

    # 把total儲存在Session中
    session['total'] = total

    return render_template('products/view_cart.html', car_list=car_list, total=total)

# 下訂單路由
@login_required
@products_bp.route('/place_order', methods=['GET', 'POST'])
def place_order():

    car_list = ShoppingCart.query.filter_by(user_id=current_user.id).all()

    total = 0

    if car_list:
        order_list = OrderList(user_id=current_user.id, total=total)
        
        for item in car_list:
            # 計算商品的總價
            item_total_price = item.product_price * item.quantity
            total += item_total_price

            order_item = OrderItem(
                product_name=item.product_name,
                product_price=item.product_price,
                quantity=item.quantity,
                total=item_total_price
            )
            order_list.order_items.append(order_item)
            db.session.delete(item)

        order_list.total = total  # 更新訂單的總價

        try:
            db.session.add(order_list)
            db.session.commit()
            
            flash('訂單已提交', category='success')
            return redirect(url_for('products.products'))
        except:
            db.session.rollback()
            flash('提交訂單時出現錯誤', category='error')
            return redirect(url_for('products.view_cart'))

    else:
        flash('購物車內尚無商品', category='error')
        return redirect(url_for('products.products'))

# 查看訂單列表路由
@login_required
@products_bp.route('/view_order', methods=['GET', 'POST'])
def view_order():

    # 取得所有已提交的訂單清單
    order_list = OrderList.query.filter_by(user_id=current_user.id, completed=False).all()

    return render_template('products/view_order.html', order_list=order_list)

# 刪除訂單路由
@login_required
@products_bp.route('/order/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = OrderList.query.get_or_404(order_id)

    # 刪除訂單內的商品細節
    for item in order.order_items:
        db.session.delete(item)

    try:
        db.session.delete(order)
        db.session.commit()
        flash('訂單已成功刪除', category='success')
    except:
        db.session.rollback()
        flash('刪除訂單時出現錯誤', category='error')
    
    return redirect(url_for('products.view_order'))

# 查看所有訂單（管理者功能）路由
@login_required
@products_bp.route('/view_all_orders', methods=['GET'])
def view_all_orders():
    # 檢查使用者是否為管理者
    if not current_user.is_admin:
        flash('權限不足', category='error')
        return redirect(url_for('products.products'))

    # 取得所有訂單清單
    order_list = OrderList.query.all()

    return render_template('products/view_all_orders.html', order_list=order_list)

# 完成訂單（管理者功能）路由
@login_required
@products_bp.route('/order/complete/<int:order_id>', methods=['POST'])
def complete_order(order_id):
    if not current_user.is_admin:
        flash('權限不足', category='error')
        return redirect(url_for('products.products'))

    order = OrderList.query.filter_by(order_id=order_id, completed=False)

    try:
        order.completed = True
        db.session.commit()
            
        flash('完成訂單成功', category='success')
    except:
        db.session.rollback()

        flash('提交訂單時出現錯誤', category='error')

    return redirect(url_for('products.view_all_orders'))



# 查看訂單歷史路由
@login_required
@products_bp.route('/order/history')
def view_order_history():

    if current_user.is_admin:
        completed_orders = OrderList.query.filter_by(completed=True).all()
    else:
        completed_orders = OrderList.query.filter_by(completed=True, user_id=current_user.id).all()

    return render_template('products/order_history.html', completed_orders=completed_orders)