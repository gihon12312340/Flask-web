# 專案名稱

這是一個使用 Flask 開發的簡單電子商務網站專案。

## 功能特點

- 使用者註冊、登入和找回密碼功能
- 商品列表和商品詳情頁面
- 購物車功能，使用者可以將商品加入購物車中
- 管理員可以編輯商品資訊，並查看所有訂單和訂單歷史

## __使用方法__ 

__註冊新帳號__  
進入 http://127.0.0.1:5000/user/register，填寫必要資料註冊新帳號。

__登入__  
進入 http://127.0.0.1:5000/user/login，使用剛剛註冊的帳號登入。

__瀏覽商品__  
在首頁 http://127.0.0.1:5000/products/ 中瀏覽商品列表。

__加入商品到購物車__  
點擊商品列表中的「加入購物車」按鈕，可以將商品加入購物車。

__管理商品__  
如果是管理員，可以進入 http://127.0.0.1:5000/products/edit 來編輯商品資訊。

__查看購物車__  
進入 http://127.0.0.1:5000/products/view_cart 查看已加入購物車的商品。

__結帳__  
進入 http://127.0.0.1:5000/products/place_order 來結帳並提交訂單。

__查看訂單__  
登入後，可以進入 http://127.0.0.1:5000/products/view_order 來查看所有已提交的訂單。

## __代碼範例__  
以下是專案中一些重要功能的程式碼範例：

__使用者登入__  
```
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        
        # 驗證會員帳號密碼是否正確
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash('登入成功', category='info')
            return redirect(url_for('user.index'))
        else:
            flash('登入失敗, 請確認帳號密碼是否正確', category='error')
    return render_template('user/login.html', form=form)
```
__提交訂單__  

```
@login_required
@products_bp.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if not current_user.is_authenticated:
        flash('驗證失敗', category='error')
        return redirect(url_for('products.products'))

    car_list = CarList.query.filter_by(user_id=current_user.id).all()

    total = 0

    if car_list:
        order_list = OrderList(product_name=" ", product_price=0, quantity=0, user_id=current_user.id, total=0)
        
        for item in car_list:
            if item.product_name is not None and item.product_price is not None and item.quantity > 0:
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


        order_list.product_price = total  # 更新訂單的商品價格
        order_list.total = total  # 更新訂單的總價

        try:
            db.session.add(order_list)
            db.session.commit()
            
            flash('訂單已提交', category='success')
            return redirect(url_for('products.products'))
        except Exception as e:
            db.session.rollback()
            flash('提交訂單時出現錯誤', category='error')
            print(str(e))

    else:
        flash('購物車內尚無商品', category='error')
        return redirect(url_for('products.products'))
```
## __預期優化項目__  
1.~~將資料庫更換為MySQL以符合實務上的需求~~  
2.將資料庫優化,如函數名稱優化,設置索引  
3.利用Redis處理需要快取的物件  

## __作者__  
這個專案由本人開發，如果有任何問題或需求，請隨時聯絡我。

## __聯絡方式__  
電子郵件：gihon12312340@gmail.com
感謝您花時間閱讀這份README，我期待在面試中展示這個專案並回答您的問題。謝謝！





