from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Contact, Blogs
# Below import is done for sending emails
from django.conf import settings
from django.core import mail
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage

# Create your views here.

# Below code refers to "Index" 
def index(request):
    return render(request, 'index.html')

# Below code refers to "About" 
def about(request):
    return render(request, 'about.html')

# Below code refers to "Contact" 
def contact(request):
    if request.method == "POST":
        fname = request.POST.get("name")
        femail = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")
        query = Contact(name=fname, email=femail,
                        phonenumber=phone, description=desc)
        query.save()

        #  Email sending code starts from here
        from_email = settings.EMAIL_HOST_USER
        connection = mail.get_connection()
        connection.open()
        
        email_message = mail.EmailMessage(
            f'Email from {fname}', f'UserEmail : {femail}\n UserPhoneNumber : {phone} \n\n\n {desc}', from_email, [
                'rupam.c3220@gmail.com', 'brk322267@gmail.com'], connection=connection)

        email_client = mail.EmailMessage(
            'Weber Technology Response', 
            'Thanks For Reaching us\n\nWeber Technology Pvt.Ltd.\n 9986786453\nreach.webertechnology.in', 
            from_email, [femail], connection=connection)
        
        connection.send_message([email_message])
        connection.close()

        messages.info(request, "Thanks For Reaching Us!")
        return redirect('/contact')
    return render(request, 'contact.html')

# Below code refers to "Signup" 
def handlesignup(request):
    if request.method == "POST":
        usernm = request.POST.get("username")
        mail = request.POST.get("email")
        passw = request.POST.get("pass1")
        conpassw = request.POST.get("pass2")

        if passw != conpassw:
            messages.warning(
                request, "Passwords are not matching, Please retype")
            return redirect('/signup')

        try:
            if User.objects.get(username=usernm):
                messages.info(
                    request, "The USERNAME you entered is already taken")
                return redirect('/signup')
        except:
            pass

        try:
            if User.objects.get(email=mail):
                messages.success(
                    request, "The EMAIL you entered is already taken")
                return redirect('/signup')
        except:
            pass
        myuser = User.objects.create_user(usernm, mail, passw)
        myuser.save()
        messages.info(request, "You have successfully Signed up, Please login")
        return redirect('/login')
    return render(request, 'signup.html')

# Below code refers to "Login" 
def handlelogin(request):
    if request.method == "POST":
        usernm = request.POST.get("username")
        passwo = request.POST.get("pass1")
        myuser = authenticate(username=usernm, password=passwo)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "You have successfully logged in!")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/login')
    return render(request, 'login.html')

# Below code refers to "Logout" 
def handlelogout(request):
    logout(request)
    messages.info(request, "You have successfully logged out!")
    return redirect('/login')

# Below code refers to "Blog" 
def handleblog(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Kindly Login")
        return redirect('/login')
    allPosts=Blogs.objects.all()
    context={'allPosts':allPosts}
    print(allPosts)
    return render(request,'blog.html',context)

# Below code refers to "Search" 
def search(request):
    query = request.GET['search']
    if len(query) >100 :
        allPosts = Blogs.objects.none()
    else:
        allPostsTitle=Blogs.objects.filter(title__icontains=query)
        allPostsDescription=Blogs.objects.filter(description__icontains=query)
        allPosts=allPostsTitle.union(allPostsDescription)        
    if allPosts.count()==0:
        messages.warning(request,"No Search Results")
    params={'allPosts':allPosts,'query':query}   
    return render(request,'search.html', params)



# Below code refers to "Services" 
def services(request):
    return render(request, 'services.html')