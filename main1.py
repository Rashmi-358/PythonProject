from flask import Flask, render_template,request
import os
from werkzeug.utils import secure_filename
import sqlite3
UPLOAD_FOLDER = 'static/upload'
import smtplib
import qrcode
import io
import base64
app = Flask(__name__,template_folder='template')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
conn = sqlite3.connect("Ceramic")
c = conn.cursor()


@app.route('/')
def home():
    return  render_template("index.html")

@app.route('/user_reg')
def home1a():
    return  render_template("User_register.html")

@app.route('/supplier_reg')
def supplier():
    return  render_template("Supplier_register.html")

@app.route('/contractor_reg')
def contractor():
    return  render_template("Contractor_register.html")

@app.route('/admin_reg')
def admin_reg():
    return  render_template("Admin_page.html")

@app.route('/admin_log')
def admin_log():
    return render_template("Admin_login.html")

@app.route('/user_log')
def user_log():
    return render_template("login.html")

@app.route('/supplier_log')
def supplier_log():
    return render_template("Supplier_login.html")

@app.route('/contractor_log')
def contractor_log():
    return render_template("Contractor_login.html")


@app.route('/admin_add_product')
def admin_add_product():
    return render_template("Add_product.html")


@app.route('/search_details/<a>')
def search_details(a):
    conn=sqlite3.connect("Ceramic")
    cur=conn.execute("SELECT * FROM tbl_product")
    rows=cur.fetchall()
    return render_template("Search_product.html",rows=rows,a=a)

@app.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        Name=request.form['uname']
        Email=request.form['uemail']
        Password=request.form['upassword']
        Mobile = request.form['umobile']
        Address = request.form['uaddress']
        conn=sqlite3.connect("Ceramic")
        conn.execute("INSERT INTO tbl_user_reg(Name,Email,Password,Mobile,Address) VALUES(?,?,?,?,?)",(Name,Email,Password,Mobile,Address))
        conn.commit()
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login("rohirockzz1995@gmail.com",
                "hnmtyebpgdzkkmcd")  # first parameter is mail id and second parametr is password message to be sent
        # message to be sent
        message = "Successfully Registered!"
        # sending the mail
        s.sendmail("rohirockzz1995@gmail.com", Email,
                   message)  # 1st parameter is sender mail 2nd one is receiver
        # terminating the session
        s.quit()



        return  render_template("login.html")

@app.route('/contractor/<a>',methods=['POST'])
def contractor_register(a):
    if request.method == 'POST':
        Name=request.form['p_name']
        Size=request.form['p_size']
        Estimation=request.form['p_est']
        Duration = request.form['p_dur']
        conn=sqlite3.connect("Ceramic")
        conn.execute("INSERT INTO tbl_contract_user(User_name,Name,Size,Estimation,Duration) VALUES(?,?,?,?,?)",(a,Name,Size,Estimation,Duration))
        conn.commit()
        return "Contract Added Successfully"



@app.route('/register_supplier',methods=['POST'])
def supplier_register():
    if request.method == 'POST':
        Name=request.form['uname']
        Email=request.form['uemail']
        Password=request.form['upassword']
        Mobile = request.form['umobile']
        Address = request.form['uaddress']
        conn=sqlite3.connect("Ceramic")
        conn.execute("INSERT INTO tbl_supplier(Name,Email,Password,Mobile,Address) VALUES(?,?,?,?,?)",(Name,Email,Password,Mobile,Address))
        conn.commit()
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login("rohirockzz1995@gmail.com",
                "hnmtyebpgdzkkmcd")  # first parameter is mail id and second parametr is password message to be sent
        # message to be sent
        message = "Successfully Registered!"
        # sending the mail
        s.sendmail("rohirockzz1995@gmail.com", Email,
                   message)  # 1st parameter is sender mail 2nd one is receiver
        # terminating the session
        s.quit()


        return  render_template("login.html")


@app.route('/admin_register',methods=['POST'])
def admin_register1():
    if request.method == 'POST':
        Email=request.form['uemail']
        Password=request.form['upassword']
        conn=sqlite3.connect("Ceramic")
        conn.execute("INSERT INTO tbl_admin(Email,Password) VALUES(?,?)",(Email,Password))
        conn.commit()
        return render_template("Admin_login.html")



@app.route('/add_product',methods=['POST'])
def add_product():
    if request.method == 'POST':
        f = request.files['ufile']
        e = f.filename
        filename = e
        filename = secure_filename(e)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        Product_name = request.form['p_name']
        Product_price = request.form['p_price']
        Product_desc = request.form['p_desc']
        conn = sqlite3.connect("Ceramic")
        conn.execute("INSERT INTO tbl_product(Image_name,Product_name,Product_price,Product_desc) VALUES(?,?,?,?)",(e,Product_name,Product_price,Product_desc))
        conn.commit()
        return "Product Added Successfully"

@app.route('/admin_login',methods=['POST'])
def admin_login():
    if request.method == 'POST':
        Email = request.form['email']
        Password = request.form['password']
        conn = sqlite3.connect('Ceramic')
        cur = conn.execute("SELECT * FROM tbl_admin WHERE Email=? AND Password=?",(Email,Password))
        rows1 = cur.fetchone()
        if rows1 == None:
            return  "Invalid Id & Password"
        else:
            return render_template('Add_product.html')




@app.route('/user_login',methods=['POST'])
def login():
    if request.method == 'POST':
        Email = request.form['uemail']
        Password = request.form['upassword']
        conn = sqlite3.connect('Ceramic')
        cur = conn.execute("SELECT * FROM tbl_user_reg WHERE Email=? AND Password=?",(Email,Password))
        rows1 = cur.fetchone()
        if rows1 == None:
            return  "Invalid Id & Password"
        else:
            cur = conn.execute("SELECT * FROM tbl_product")
            rows = cur.fetchall()
            return render_template('Product_details.html',rows1=rows1,rows=rows)


@app.route('/supplier_login',methods=['POST'])
def logindd():
    if request.method == 'POST':
        Email = request.form['uemail']
        Password = request.form['upassword']
        conn = sqlite3.connect('Ceramic')
        cur = conn.execute("SELECT * FROM tbl_supplier WHERE Email=? AND Password=?",(Email,Password))
        rows1 = cur.fetchone()
        if rows1 == None:
            return  "Invalid Id & Password"
        else:
            cur = conn.execute("SELECT * FROM tbl_product")
            rows = cur.fetchall()
            return render_template('Product_details_supplier.html',rows1=rows1,rows=rows)




@app.route('/add/<a>/<b>')
def add(a,b):
    conn = sqlite3.connect("Ceramic")
    cur = conn.execute("SELECT * FROM tbl_product WHERE Product_id=?",(a,))
    row = cur.fetchone()
    return render_template("Cart.html",row=row,b=b)

@app.route('/add_to_cart/<prod>/<cust>',methods=["POST"])
def add_to_cart(prod,cust):
    if request.method=='POST':
        qty = request.form['quantity']
        conn=sqlite3.connect("Ceramic")
        cur = conn.execute("SELECT * FROM tbl_product WHERE Product_id=?",(prod,))
        row = cur.fetchone()
        cur = conn.execute("SELECT * FROM tbl_user_reg WHERE Name=?", (cust,))
        rows = cur.fetchone()
        conn.execute("INSERT INTO tbl_cart(c_name,p_name,qty,price,customer_address)VALUES(?,?,?,?,?)",(rows[1], row[2], qty, row[3], rows[5]))
        conn.commit()
        cur = conn.execute("SELECT * FROM tbl_user_reg WHERE Name=?",(cust,))
        rows1 = cur.fetchone()
        cur = conn.execute("SELECT * FROM tbl_product")
        rows = cur.fetchall()
        return render_template("Product_details.html",rows1=rows1,rows=rows)

@app.route('/checkout/<a>')
def  checkout(a):
    conn = sqlite3.connect("Ceramic")
    cur = conn.execute("SELECT * FROM tbl_cart WHERE c_name=?",(a,))
    rows = cur.fetchall()
    cur = conn.execute("SELECT * FROM tbl_user_reg WHERE Name=?",(a,))
    mail = cur.fetchone()
    print(mail)
    if rows == None:
        return render_template("Bill.html",a=a,msg="U Seleced Nothing!")
    else:
        total = 0
        for row in rows:
            print(row)
            total = (int(row[3])*int(row[4]))+total



        for row in rows:
            conn.execute("INSERT INTO tbl_bill(C_name,Product_name,Product_qty,Product_price,Total_price,Address)VALUES(?,?,?,?,?,?)", (a,row[2],row[3],row[4],total,row[5]))
            conn.commit()
        conn.execute("DELETE FROM tbl_cart WHERE c_name=?",(a,))
        conn.commit()
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login("rohirockzz1995@gmail.com","hnmtyebpgdzkkmcd")

        message = "Your Order is Confirmed \n" + "Item \t \t" + "Quantity \t \t" + "Price \t \t \n"
        for row in rows:
            message=message+row[2]+"\t"+row[3]+"\t"+row[4]+"\n"
        message=message+"\n"+"Total Amount Is"+str(total)
        # sending the mail
        s.sendmail("rohirockzz1995@gmail.com", mail[2],
                   message)
        # terminating the session
        s.quit()

        return render_template("Bill.html",rows=rows,total=total,a=a)

@app.route('/bill_histry/<a>')
def bill_histry(a):
    conn=sqlite3.connect("Ceramic")
    cur = conn.execute("SELECT * FROM tbl_bill WHERE C_name=?",(a,))
    rows = cur.fetchall()
    print(rows)
    if rows == []:
        cust=[]
        return render_template("Bill_histry.html",a=a,msg="U Dont have any order histry!",cust=cust)
    else:
        cust = rows[0]
        return render_template("Bill_histry.html",rows=rows,cust=cust,a=a)


@app.route('/supplier_bill_histry/<a>')
def supplier_bill_histry(a):
    conn=sqlite3.connect("Ceramic")
    cur = conn.execute("SELECT * FROM tbl_book WHERE Supplier_name=?",(a,))
    rows = cur.fetchall()
    print(rows)
    if rows == []:
        cust=[]
        return render_template("Bill_histry_supplier.html",a=a,msg="U Dont have any order histry!",cust=cust)
    else:
        cust = rows[0]
        return render_template("Bill_histry_supplier.html",rows=rows,cust=cust,a=a)


@app.route('/home/<a>')
def home1(a):
    conn = sqlite3.connect('Ceramic')
    cur = conn.execute("SELECT * FROM tbl_user_reg WHERE Name=?", (a,))
    rows1 = cur.fetchone()
    cur = conn.execute("SELECT * FROM tbl_product")
    rows = cur.fetchall()
    return render_template('Product_details.html',rows1=rows1,rows=rows)




@app.route('/add_contract/<a>')
def add_contract(a):
    conn = sqlite3.connect('Ceramic')
    cur = conn.execute("SELECT * FROM tbl_user_reg WHERE Name=?", (a,))
    rows1 = cur.fetchone()
    return render_template('Contract.html',rows1=rows1)

@app.route('/product_details/<a>')
def product_details(a):
    conn = sqlite3.connect('Ceramic')
    cur = conn.execute("SELECT * FROM tbl_user_reg WHERE Name=?", (a,))
    rows1 = cur.fetchone()
    cur = conn.execute("SELECT * FROM tbl_product")
    rows = cur.fetchall()
    return render_template('Product_details.html',rows1=rows1,rows=rows)

@app.route('/supplier_product_details/<a>')
def supplier_product_details(a):
    conn = sqlite3.connect('Ceramic')
    cur = conn.execute("SELECT * FROM tbl_supplier WHERE Name=?", (a,))
    rows1 = cur.fetchone()
    cur = conn.execute("SELECT * FROM tbl_product")
    rows = cur.fetchall()
    return render_template('Product_details_supplier.html',rows1=rows1,rows=rows)


@app.route('/purchase_list')
def purchase_list():
    conn = sqlite3.connect('Ceramic')
    cur = conn.execute("SELECT * FROM tbl_bill")
    rows = cur.fetchall()
    return render_template('Purchase_details.html',rows=rows)

@app.route('/user_list')
def user_list():
    conn = sqlite3.connect('Ceramic')
    cur = conn.execute("SELECT * FROM tbl_user_reg")
    rows = cur.fetchall()
    return render_template('User_details.html',rows=rows)

@app.route('/contract_user_list')
def contract_user_list():
    conn = sqlite3.connect('Ceramic')
    cur = conn.execute("SELECT * FROM tbl_contract_user")
    rows = cur.fetchall()
    return render_template('Admin_user_contract_details.html',rows=rows)


@app.route('/supplier_list')
def suppler_list():
    conn = sqlite3.connect('Ceramic')
    cur = conn.execute("SELECT * FROM tbl_supplier")
    rows = cur.fetchall()
    return render_template('Admin_supplier_details.html',rows=rows)


@app.route('/bill_list_supplier')
def bill_list_supplier():
    conn = sqlite3.connect('Ceramic')
    cur = conn.execute("SELECT * FROM tbl_admin_bill")
    rows = cur.fetchall()
    return render_template('Admin_supplier_bill.html',rows=rows)

@app.route('/supplier_order_list')
def suppler_order():
    conn = sqlite3.connect('Ceramic')
    cur = conn.execute("SELECT * FROM tbl_book")
    rows = cur.fetchall()
    return render_template('Admin_supplier_order.html',rows=rows)

@app.route('/product_list')
def product_list():
    conn = sqlite3.connect('Ceramic')
    cur = conn.execute("SELECT * FROM tbl_product")
    rows = cur.fetchall()
    return render_template('Admin_product_details.html',rows=rows)

@app.route('/search_product/<a>',methods=['POST'])
def search_product(a):
    if request.method=='POST':
        Product_name=request.form['u_product']
        conn=sqlite3.connect("Ceramic")
        cur=conn.execute("SELECT * FROM tbl_product WHERE Product_name=?",(Product_name,))
        rows=cur.fetchall()
        return render_template("Search_product.html",rows=rows,a=a)

@app.route('/delete_user/<a>')
def delete_user(a):
    conn=sqlite3.connect("Ceramic")
    conn.execute("DELETE FROM tbl_user_reg WHERE User_id=?",(a,))
    conn.commit()
    return "Data Deleted Successfully"

@app.route('/delete_purchase/<a>')
def delete_purchase(a):
    conn=sqlite3.connect("Ceramic")
    conn.execute("DELETE FROM tbl_bill WHERE Bill_id=?",(a,))
    conn.commit()
    return "Data Deleted Successfully"

@app.route('/delete_product/<a>')
def delete_product(a):
    conn=sqlite3.connect("Ceramic")
    conn.execute("DELETE FROM tbl_product WHERE Product_id=?",(a,))
    conn.commit()
    return "Data Deleted Successfully"


@app.route('/book_room/<a>')
def add_room(a):
    conn = sqlite3.connect("Ceramic")
    cur = conn.execute("SELECT * FROM tbl_bill WHERE Bill_id=?",(a,))
    row = cur.fetchone()

    return render_template("Material_order.html",row=row)



@app.route('/make_bill/<a>')
def Make_bil(a):
    conn = sqlite3.connect("Ceramic")
    cur = conn.execute("SELECT * FROM tbl_book WHERE B_id=?",(a,))
    row = cur.fetchone()

    return render_template("Supplier_make_bill.html",row=row)

@app.route('/add_book/<cust>', methods=["POST"])
def add_room_book(cust):
    if request.method == 'POST':
        Supplier_name = request.form['u_s_name']
        Date = request.form['udate']
        conn = sqlite3.connect("Ceramic")
        cur = conn.cursor()

        # Fetch the current bill to get the user and total amount
        cur.execute("SELECT * FROM tbl_bill WHERE Bill_id=?", (cust,))
        row = cur.fetchone()

        if row:
            user_name = row[1]  # Assuming this is the user name
            current_total = float(row[5])  # Assuming Total_amount is in column index 5

            # Calculate new total
            new_total = current_total - 0

            # Insert EMI record
            cur.execute("INSERT INTO tbl_book(User_name, Material_name,Qty,Supplier_name,Date) VALUES (?,?,?, ?, ?)",
                        (user_name, row[2],row[3],Supplier_name,Date))

            # Update the total amount in tbl_bill


            conn.commit()
            conn.close()
            return "Material Order Requested To Supplier Successfully"
        else:
            conn.close()
            return "Bill ID not found", 404



@app.route('/add_admin_bill/<cust>', methods=["POST"])
def add_room_book12(cust):
    if request.method == 'POST':
        Date = request.form['udate']
        Price = float(request.form['upaid'])
        Balance = float(request.form['ubalance'])
        conn = sqlite3.connect("Ceramic")
        cur = conn.cursor()

        # Fetch the current bill to get the user and total amount
        cur.execute("SELECT * FROM tbl_book WHERE B_id=?", (cust,))
        row = cur.fetchone()

        if row:
            user_name = row[4]  # Assuming this is the user name
            current_total = float(row[3])  # Assuming Total_amount is in column index 5

            # Calculate new total
            new_total = 0

            # Insert EMI record
            cur.execute("INSERT INTO tbl_admin_bill(Supplier_name, Material_name,Date, Qty,Price, Balance) VALUES (?,?,?, ?, ?,?)",
                        (user_name, row[2],Date, row[3],Price, Balance))

            # Update the total amount in tbl_bill


            conn.commit()
            conn.close()
            return "Bill Added Successfully"
        else:
            conn.close()
            return "Bill ID not found", 404


@app.route('/payment', methods=['POST'])
def payment():
    import qrcode, io, base64

    amount = request.form['amount']
    customer = request.form['customer']
    method = request.form.get('payment_method')

    if method == "UPI":
        upi_id = "yourupiid@bank"
        payee_name = "Your Business Name"
        upi_link = f"upi://pay?pa={upi_id}&pn={payee_name}&am={amount}&cu=INR"

        # Generate QR code
        qr = qrcode.make(upi_link)
        img_io = io.BytesIO()
        qr.save(img_io, 'PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode()

        return f"""
        <h2>Scan to Pay ₹{amount}</h2>
        <img src="data:image/png;base64,{img_base64}">
        <p><strong>Customer:</strong> {customer}</p>
        <p><strong>Payment Method:</strong> UPI</p>
        """
    else:
        return f"""
        <h2>Payment Details</h2>
        <p><strong>Customer:</strong> {customer}</p>
        <p><strong>Amount:</strong> ₹{amount}</p>
        <p><strong>Payment Method:</strong> {method}</p>
        <p>Please collect confirmation after payment.</p>
        """


@app.route('/logout')
def logout():
    return render_template("index.html")

if __name__=="__main__":
    app.run(host="0.0.0.0")