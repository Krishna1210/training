from odoo import http
from odoo.http import request


class Realestate(http.Controller):

    @http.route('/hello', auth="public")
    def hello(self, **kw):
        return "Hello World"

    @http.route('/hello_user', auth="user")
    def hello_user(self, **kw):
        return "Hello %s" % (request.env.user.name)
  

    @http.route('/hello_template_user', website=True )
    def hello_template_user(self, **kw):
        property = request.env['estate.properties'].search([('state', '=', 'sold'), ('expected_price', '>' ,'2000')])
        print ("properties ::: ", property)
        return request.render('Real_estate.real_estate_properties_list', { 'user': request.env.user, 'abc': property }) 
    
    @http.route('/properies' , website=True)
    def Real_estate_properties(self, **kw):
        return request.render('Real_estate.properties_templet', {})