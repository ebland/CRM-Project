@app.route('/dashboard')
def dashboard():
    admin_logged_in = current_user.session([roles.roles_1])

    #to do....specify what roles estimator and other permissions 1,2,3 will see on dashboard...
    staff_logged_in = current_user.session([roles.roles_2])
    login_form = request.form.get('login_form')

    #need to check before adding to server.py if this will set session correctly
    #ask Leslie if this way or the one below will work better with user_roles we set up
    user = users.get_current_user()
        if user:
            if Customer.get_by_email(user.email()):
                self.redirect("/templates/customer_profile")

    return render_template('dashboard.html',
                           icon="fa fa-dashboard",
                           module_abbreviation="ECRM",
                           module_name="ECRM Client Management",
                           page_name="Dashboard",
                           login_form=login_form,
                           current_user=current_user,
                           logged_in=logged_in)


@app.route('/staff_dashboard', methods=['GET', 'POST'])
admin_logged_in = current_user.session([roles.roles_1])
staff_logged_in = current_user.session([roles.roles_2])

def user_management():
    admin_logged_in = current_user.session([roles.roles_1])
    staff_logged_in = current_user.session([roles.roles_2])
    login_form = request.form.get('login_form')
    delete_form = request.form.get('update_user')
    forms = {'Create_new_user': create_new_user,
             'Create_new_user': update_user,
             'Delete_User_Form'    : update_user
    
    try:
        customers = db.session.query(Customers).all()
       
    except:
        customers = {"-": {"timestamp": "-", "fname": "-", "lname": "-", "phone": "-"}}

    if request.method == 'POST':
        if request.form['form_submit']:

            if request.form['form_submit'] == 'creat_new_user':
                admin_logged_in = current_user.session([roles.roles_1])
                staff_logged_in = current_user.session([roles.roles_2])
                permissions = True

                if admin_logged_in or staff_logged_in == True:
                    if create_new_user.validate_on_submit():
                        add_customer(create_new_user)
                    else:
                        flash('Error. No changes or additions submitted.', 'danger')

            elif request.form['form_submit'] == 'Delete_User_Form':
                admin_logged_in = current_user.session([roles.roles_1])
                staff_logged_in = current_user.session([roles.roles_2])              
                
                if admin_logged_in or staff_logged_in == False:
                    flash('You do not have sufficient permissions.', 'danger')
                elif admin_logged_in or staff_logged_in == True:
                    if delete_form.validate_on_submit():
                        delete_customer(update_user)
                    else:
                        flash('Deletion unsuccessful', 'danger')
                else:
                    flash('Access Denied.Your IP has been recorded and sent to Admin. '
                          'Please wait for Admin to advise next steps.', 'danger')

            elif request.form['form_submit'] == 'create_new_user':
                admin_logged_in = current_user.session([roles.roles_1])
                staff_logged_in = current_user.session([roles.roles_2])  
                permissions = True

                if admin_logged_in or staff_logged_in == True:
                    if update_form.validate_on_submit():
                        update_user(update_user)
                    else:
                        flash('Deletion unsuccessful', 'danger')

            else:
                flash('An error rendered after submitting the user update.'
                      'Contact the admin or try again if you know the reason for the error.', danger')
        else:
            flash('Error. What form were you trying to submit. '
                  ' Please contact the application administrator.', 'danger')
        return redirect((url_for('/dashboard')))



    if request.path == '/templates':
        url = '/all_users.html'
        

    else:
        url = '/show_user.html'
            

    # return render_template('dashboard.html',
    #                        icon="http://gravatar",
    #                        module_abbreviation="ECRM",
    #                        page_name="ECRM Dashboard",
    #                        form_title="Customer",
    #                        users=users,
    #                        login_form=login_form,
    #                        current_user=current_user,
    #                        logged_in=logged_in)


   

                          
                          
                           
                           
                           
                          
                         
                         
