from django.shortcuts import render
from .forms import *
from django.contrib import messages
from .models import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import datetime


# Default function
def log(request):
    print(request)
    if request.method == 'POST':
        print(request.POST)

        # User Sign Up
        try:
            if request.POST['s2'] == 'Sign_Up':
                form = Signupform(request.POST)
                print(form.errors)
                if form.is_valid():
                    pwd = request.POST['password']
                    passw = str(pwd)
                    # Minimum password length is 8
                    if len(passw) < 8:
                        error_msg3 = "Minimum length of password is 8. Please sign up again!"
                        messages.error(request, error_msg3)
                        return redirect('/')
                    # Cannot sign up if user is existing
                    elif User.objects.filter(username=request.POST.get('username')).exists():
                        error_msg4 = "User already exists! Try a different username..."
                        messages.error(request, error_msg4)
                        return redirect('/')
                    # Signing up
                    else:
                        user = User(username=request.POST['username'], password=request.POST['password'],
                                    email=request.POST['email'])
                        user.set_password(request.POST['password'])
                        user.save()
                        userdetails = Userdetails(user=user, email=request.POST['email'],
                                                  password=request.POST['password'])
                        userdetails.save()

                        try:
                            users = User.objects.get(username=request.POST.get('username'))
                        except:
                            error_msg = "Wrong details"
                            messages.error(request, error_msg)
                            return redirect('/')
                        # Authenticating the Signed in user
                        users = authenticate(username=users.username, password=request.POST.get('password'))
                        if users is not None:
                            login(request, users)
                            try:
                                udets = User.objects.filter(username=users.username)
                            except:
                                error_msg = "Wrong details"
                                messages.error(request, error_msg)
                            return render(request, 'spoken/userpage.html', {'udets': udets})
                        else:
                            return redirect('/')

                else:
                    form = Signupform()
                    errors = form.errors
                    print(errors)
                    return redirect('/')

            # Admin Sign In
            elif request.POST['s2'] == 'Continue':
                form = Adminform(request.POST)
                print(form.errors)
                if form.is_valid():
                    user1 = request.POST.get('user1')
                    pwd = request.POST.get('pwd')
                    # Creating our own Admin with username: sanya and password: sanya5549
                    if user1 == 'sanya' and pwd == 'sanya5549':
                        list1 = Userdetails.objects.all()
                        list2 = Foss.objects.all()
                        errors = None
                        print(request.POST)
                        return render(request, 'spoken/admin.html', {'list2': list2, 'list1': list1})

                    # If username or password is wrong, redirecting to login page
                    else:
                        error_msg2 = "Wrong Admin Credentials"
                        messages.error(request, error_msg2)
                        return redirect('/')
                else:
                    return redirect('/')

            # User Log In
            elif request.POST['s2'] == 'Log_In':
                try:
                    # creating User object
                    users = User.objects.get(username=request.POST.get('user2'))
                except:
                    error_msg = "Wrong details"
                    messages.error(request, error_msg)
                    return redirect('/')
                # Authenticating the user
                users = authenticate(username=users.username, password=request.POST.get('pass2'))
                print(users)
                # Returning the details of user
                if users is not None:
                    login(request, users)
                    f_name = ''
                    Mainlist1 = []
                    list1 = Userdetails.objects.all()
                    list4 = Tutorialdetails.objects.all()
                    udets = User.objects.filter(username=users.username)
                    print(udets)
                    for k in list1:
                        if k.user == User.objects.get(username=request.POST.get('user2')):
                            print(k.fossname)
                            f_name = k.fossname
                            if f_name is None:
                                am = 0
                            else:
                                user2 = User.objects.filter(username=request.POST.get('user2'))
                                print(user2)
                                # Fetching amount of that user
                                aw = Payment.objects.get(user=Userdetails.objects.get(user=user2[0]))
                                am = aw.amount
                                print(am, "am")

                    for u1 in list4:
                        Dict = {}
                        if u1.fossname == f_name:
                            Dict['b1'] = u1.tname  # For tutorial name
                            Dict['b2'] = u1.fossname  # For foss name
                            Dict['b3'] = u1.submdate  # For  name submission date
                            Dict['b4'] = u1.deadline  # For deadline provided by admin (sanya)
                            Mainlist1.append(Dict)

                    return render(request, 'spoken/userpage.html', {'Mainlist1': Mainlist1, 'udets': udets, 'f_name': f_name, 'am':am})

                else:
                    # User is existing but password is wrong
                    error_msg2 = "Incorrect Password"
                    messages.error(request, error_msg2)
                    return redirect('/')
        except:
            pass

    else:
        return render(request, 'spoken/login.html')


# For fetching and returning data in user page
def userpg(request):
    if request.method == 'POST':
        try:
            # if the user Uploads the tutorial
            if request.POST['s5']:
                tut_name = request.POST['tutname']  # Fetching tutorial name
                foss_name = request.POST['fname']  # Fetching foss name of that tutorial
                # If the particular tutorial with fossname exists in table Tutorialdetails
                if Tutorialdetails.objects.filter(tname=tut_name, fossname=foss_name).exists():
                    # Creating object of that entry in table Tutorialdetails to enter submission date
                    tt = Tutorialdetails.objects.get(tname=tut_name, fossname=foss_name)
                    if tt.submdate is None:
                        tt.submdate = datetime.date.today()
                        tt.save()  # Submission date entered
                        u2 = Userdetails.objects.get(fossname=foss_name)
                        # Updating the total amount
                        list6 = Tutorialdetails.objects.filter(fossname=foss_name)
                        c = 0
                        for i in list6:
                            if i.submdate is not None:
                                print(i)
                                if i.submdate <= i.deadline:
                                    c+=1000
                                    amtt = Payment.objects.get(user=u2)
                                    amtt.amount = c
                                    amtt.save()

                        error_msg20 = " Tutorial Uploaded successfully.."
                        messages.error(request, error_msg20)
                    # Not allowing a user to upload the tutorial again
                    else:
                        error_msg19 = " Tutorial already Submitted"
                        messages.error(request, error_msg19)
                    # Fetching details i.e. tutorial names, foss name, amount of the logged in user
                    Mainlist2 = []
                    list7 = Tutorialdetails.objects.all()
                    try:
                        # Creating object of logged in user being received by hidden type in userpage.html
                        users = User.objects.get(username=request.POST['usernm'])
                    except:
                        pass
                    udets = User.objects.filter(username=users.username)
                    print(udets)

                    for u1 in list7:
                        Dict = {}
                        if str(u1.fossname) == str(foss_name):
                            Dict['b1'] = u1.tname  # For tutorial name
                            Dict['b2'] = u1.fossname  # For foss name
                            Dict['b3'] = u1.submdate  # For  name submission date
                            Dict['b4'] = u1.deadline  # For deadline provided by admin (sanya)
                            Mainlist2.append(Dict)
                        else:
                            print('not exists')
                    # Fetching total amount of that user
                    user2 = User.objects.filter(username=request.POST['usernm'])
                    aww = Payment.objects.get(user=Userdetails.objects.get(user=user2[0]))
                    amm = aww.amount
                    return render(request, 'spoken/userpage.html', {'Mainlist1': Mainlist2, 'udets': udets, 'f_name': foss_name, 'am': amm})
        except:
            pass


# For fetching and returning data in admin page
def admindata(request):
    if request.method == 'POST':
        print(request.POST)
        try:
            list1 = Userdetails.objects.all()  # Fetching all the users to check their details and assigning them a foss
            list2 = Foss.objects.all()  # Fetching all the foss
            print(request.POST)
            # For creating a foss
            if request.POST['s3'] == 'Submit_Foss':
                form = Createform(request.POST)
                print(form.errors)
                # Two tutorial names of a foss cannot be same
                if form.is_valid():
                    tutt = [request.POST.get('tutorial1'), request.POST.get('tutorial2'), request.POST.get('tutorial3'),
                            request.POST.get('tutorial4'), request.POST.get('tutorial5'), request.POST.get('tutorial6'),
                            request.POST.get('tutorial7'), request.POST.get('tutorial8'), request.POST.get('tutorial9'),
                            request.POST.get('tutorial10')]

                    # Duplicate names will not be entered in seen array
                    seen = []
                    for tt in tutt:
                        if tt in seen:
                            # As the tutorial names clash, returning the same page without foss being created
                            error_msg12 = "Tutorial names can't be same... Please correct it!!"
                            messages.error(request, error_msg12)
                            return render(request, 'spoken/admin.html', {'list1': list1, 'list2': list2})
                        else:
                            seen.append(tt)

                # If a foss has been assigned to a user, it can't be created anymore
                # (one to one relationship between user and foss)
                if Foss.objects.filter(fossname=request.POST.get('fossid')).exists():
                    error_msg11 = "Foss already exists! Try a different name..."
                    messages.error(request, error_msg11)
                    return render(request, 'spoken/admin.html', {'list1': list1, 'list2': list2})

                # Creating foss
                elif form.is_valid():
                    foss22 = Foss(fossname=request.POST['fossid'])
                    foss22.save()
                    t1 = Tutorialdetails(fossname=foss22, tname=request.POST['tutorial1'],
                                         deadline=request.POST['deadline1'])
                    t2 = Tutorialdetails(fossname=foss22, tname=request.POST['tutorial2'],
                                         deadline=request.POST['deadline2'])
                    t3 = Tutorialdetails(fossname=foss22, tname=request.POST['tutorial3'],
                                         deadline=request.POST['deadline3'])
                    t4 = Tutorialdetails(fossname=foss22, tname=request.POST['tutorial4'],
                                         deadline=request.POST['deadline4'])
                    t5 = Tutorialdetails(fossname=foss22, tname=request.POST['tutorial5'],
                                         deadline=request.POST['deadline5'])
                    t6 = Tutorialdetails(fossname=foss22, tname=request.POST['tutorial6'],
                                         deadline=request.POST['deadline6'])
                    t7 = Tutorialdetails(fossname=foss22, tname=request.POST['tutorial7'],
                                         deadline=request.POST['deadline7'])
                    t8 = Tutorialdetails(fossname=foss22, tname=request.POST['tutorial8'],
                                         deadline=request.POST['deadline8'])
                    t9 = Tutorialdetails(fossname=foss22, tname=request.POST['tutorial9'],
                                         deadline=request.POST['deadline9'])
                    t10 = Tutorialdetails(fossname=foss22, tname=request.POST['tutorial10'],
                                          deadline=request.POST['deadline10'])
                    if t1 is not None and t2 is not None and t3 is not None and t4 is not None and t5 is not None and t6 is not None and t7 is not None and t8 is not None and t9 is not None and t10 is not None:
                        t1.save()
                        t2.save()
                        t3.save()
                        t4.save()
                        t5.save()
                        t6.save()
                        t7.save()
                        t8.save()
                        t9.save()
                        t10.save()
                        error_msg9 = "Foss Created Successfully..!"
                        messages.error(request, error_msg9)
                        return render(request, 'spoken/admin.html', {'list1': list1, 'list2': list2})

                    # If a valid date format is not entered, the data won't be accepted
                    else:
                        error_msg13 = "Please enter valid format of date....!"
                        messages.error(request, error_msg13)
                        return render(request, 'spoken/admin.html', {'list1': list1, 'list2': list2})

                else:
                    error_msg5 = "Data not saved.. Some format is worng..!"
                    messages.error(request, error_msg5)
                    return render(request, 'spoken/admin.html', {'list1': list1, 'list2': list2})

            # Assigning foss to a particular user
            elif request.POST['s3'] == 'Assign_Foss':
                form = Assignform(request.POST)
                print(form.errors)
                list5 = Userdetails.objects.all()
                for u in list5:

                    # New foss will not be assigned to a user, if already assigned once (One to one Relationship)
                    if u.user == User.objects.get(username=request.POST.get('userassn')) and u.fossname is not None:
                        error_msg14 = "Foss already assigned!"
                        messages.error(request, error_msg14)
                        return render(request, 'spoken/admin.html', {'list1': list1, 'list2': list2})

                # If a foss has been assigned to a user, it can't be assigned anymore
                if Userdetails.objects.filter(fossname=request.POST.get('fossassn')).exists():
                    error_msg16 = "This Foss has been already assigned to a user!"
                    messages.error(request, error_msg16)
                    return render(request, 'spoken/admin.html', {'list1': list1, 'list2': list2})

                # Assigning foss to a user
                elif form.is_valid():
                    use1 = User.objects.only('username').get(username=request.POST['userassn'])
                    use = Foss.objects.only('fossname').get(fossname=request.POST['fossassn'])
                    obj = Userdetails(user=use1, fossname=use)
                    obj.save()
                    obj2 = Payment(user_id=use1.id)
                    obj2.save()
                    error_msg10 = "Foss Assigned Successfully..!"
                    messages.error(request, error_msg10)
                    return render(request, 'spoken/admin.html', {'list1': list1, 'list2': list2})

                else:
                    form = Assignform()
                    errors = form.errors
                    print(errors)
                    error_msg11 = "Something is wrong...!"
                    messages.error(request, error_msg11)
                    return render(request, 'spoken/admin.html', {'list1': list1, 'list2': list2})

        except:
            pass

        try:
            # To fetch user details present in the list
            if request.POST['s4']:
                list1 = Userdetails.objects.all()
                list4 = Tutorialdetails.objects.all()
                Mainlist = []

                # Fetching foss name of that particular user
                for u in list1:
                    if u.user == User.objects.get(username=request.POST.get('s4')):
                        foss_name = u.fossname
                        print(foss_name)

                # If foss has been assigned, fetching all the details
                if foss_name is not None:
                    for u1 in list4:
                        Dict = {}
                        if u1.fossname == foss_name:
                            Dict['a1'] = u1.tname
                            Dict['a2'] = u1.fossname
                            Dict['a3'] = u1.submdate
                            Dict['a4'] = u1.deadline
                            Mainlist.append(Dict)
                            print("giudfy")

                        else:
                            error_msg6 = "please choose the user"

                    user2 = User.objects.filter(username=request.POST.get('s4'))
                    aw = Payment.objects.get(user=Userdetails.objects.get(user=user2[0]))
                    am = aw.amount

                # If foss has not been assigned, no foss or tutorial data
                else:
                    return render(request, 'spoken/admin.html',{'list1': list1, 'list2': list2})

                return render(request, 'spoken/admin.html', {'Mainlist': Mainlist, 'list1': list1, 'list2': list2, 'am':am})
        except:
            pass