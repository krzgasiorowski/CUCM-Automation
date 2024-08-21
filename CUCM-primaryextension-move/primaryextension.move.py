from ciscoaxl import axl

cucm1 = 'x.x.x.x'
username1 = 'axlaccess'
password1 = 'password'
version1 = '11.0'
ucm1 = axl(username=username1,password=password1,cucm=cucm1,cucm_version=version1)

cucm2 = 'y.y.y.y'
username2 = 'axlaccess'
password2 = 'password'
version2 = '12.5'
ucm2 = axl(username=username2,password=password2,cucm=cucm2,cucm_version=version2)

for user in ucm1.get_users():
    userfull = ucm1.get_user(userid=user.userid)
#    print(userfull)
    print(userfull.userid,userfull.primaryExtension,userfull.primaryExtension)
    ucm2.update_user(userid=userfull.userid, primaryExtension=userfull.primaryExtension,ipccExtension=userfull.ipccExtension['_value_1'],ipccRoutePartition={'_value_1': 'IPPHONE'})
