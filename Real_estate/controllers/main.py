from odoo import http
from odoo.http import request


class Realestate(http.Controller):

    @http.route('/hello', auth="public")
    def hello(self, **kw):
        return "Hello World"

    @http.route('/hello_user', auth="user")
    def hello_user(self, **kw):
        return "Hello %s" % (request.env.user.name)

    @http.route('/hello_template_user', website=True)
    def hello_template_user(self, **kw):
        property = request.env['estate.properties'].search(
            [('state', '=', 'sold'), ('expected_price', '>', '2000')])
        print("properties ::: ", property)
        return request.render('Real_estate.real_estate_properties_list', {'user': request.env.user, 'property': property})

    @http.route('/properties', website=True)
    def Real_estate_properties(self, **kw):
        property = request.env['estate.properties'].search([])
        return request.render('Real_estate.properties_templet', {'user': request.env.user, 'abc': property})

    @http.route('/properties/<model("estate.properties"):property>', auth="public", website=True, method=['POST'])
    def property(self, property=False, **kw):
        print("\n value is print***************************************")
        if property:
                return request.render('Real_estate.property_details', {
                    'pr': property
                })

    @http.route('/property/add', auth="public", website=True)
    def partner_form(self, **post):
        return request.render("Real_estate.tmp_property_form", {})

    @http.route('/property/form/submit', auth="public", website=True)
    def property_form_submit(self, **post):
        partner = request.env['estate.properties'].create({
            'name': post.get('name'),
            'expected_price': post.get('expected_price'),
        })
        print("PRINT :::", post)
        vals = {
            'partner': partner,
        }
        return request.render("Real_estate.tmp_property_form", vals)
