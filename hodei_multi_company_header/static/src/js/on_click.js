odoo.define('hodei_multi_company_header.SwitchCompanyMenu', function(require) {
"use strict";

/**
 * When Odoo is configured in multi-company mode, users should obviously be able
 * to switch their interface from one company to the other.  This is the purpose
 * of this widget, by displaying a dropdown menu in the systray.
 */

var config = require('web.config');
var core = require('web.core');
var session = require('web.session');
var SystrayMenu = require('web.SystrayMenu');
var SwitchCompanyMenu = require('web.SwitchCompanyMenu');

var _t = core._t;

SwitchCompanyMenu.include({
    start: function () {
        //var companiesList = '';
        //if (this.isMobile) {
        //    companiesList = '<li class="bg-info">' +
        //        _t('Tap on the list to change company') + '</li>';
        //}
        //else {
        //    this.$('.oe_topbar_name').text(session.user_companies.current_company[1]);
        //}
        //_.each(session.user_companies.allowed_companies, function(company) {
        //    var a = '';
        //    if (company[0] === session.user_companies.current_company[0]) {
        //        a = '<i class="fa fa-check mr8"></i>';
        //    } else {
        //        a = '<span style="margin-right: 24px;"/>';
        //    }
        //    companiesList += '<a role="menuitem" href="#" class="dropdown-item" data-menu="company" data-company-id="' +
        //                    company[0] + '">' + a + company[1] + '</a>';
        //});
        if (session.user_companies.current_company[0] == 1)
        {
            this.$('.dropdown-menu').parent().parent().parent().parent().find('.o_main_navbar').removeClass('header-company-marsan').addClass('header-company-negoce');
        }
        else if (session.user_companies.current_company[0] == 3)
        {
            this.$('.dropdown-menu').parent().parent().parent().parent().find('.o_main_navbar').removeClass('header-company-negoce').addClass('header-company-marsan');
        }
        //this.$('.dropdown-menu').html(companiesList);
        return this._super();
    },
    // _onClick: function (ev) {
    //     ev.preventDefault();
    //     var companyID = $(ev.currentTarget).data('company-id');
    //     if (companyID == 1)
    //     {
    //         $(ev.currentTarget).parent().parent().parent().parent().find('.o_main_navbar').removeClass('header-company-marsan').addClass('header-company-negoce');
    //     }
    //     else if (companyID == 3)
    //     {
    //         $(ev.currentTarget).parent().parent().parent().parent().find('.o_main_navbar').removeClass('header-company-negoce').addClass('header-company-marsan');
    //     }
    //     this._rpc({
    //         model: 'res.users',
    //         method: 'write',
    //         args: [[session.uid], {'company_id': companyID}],
    //     })
    //     .then(function() {
    //         location.reload();
    //     });
    // },
});

//SystrayMenu.Items.push(SwitchCompanyMenu);
return SwitchCompanyMenu;

});
