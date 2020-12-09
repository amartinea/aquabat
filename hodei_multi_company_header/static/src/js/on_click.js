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
    _onClick: function (ev) {
        ev.preventDefault();
        var companyID = $(ev.currentTarget).data('company-id');
        if (companyID == 1)
        {
            $(ev.currentTarget).parent().parent().parent().parent().removeClass('header-company-marsan').addClass('header-company-negoce');
        }
        else if (companyID == 3)
        {
            $(ev.currentTarget).parent().parent().parent().parent().removeClass('header-company-negoce').addClass('header-company-marsan');
        }
        this._rpc({
            model: 'res.users',
            method: 'write',
            args: [[session.uid], {'company_id': companyID}],
        })
        .then(function() {
            location.reload();
        });
    },
});

SystrayMenu.Items.push(SwitchCompanyMenu);
return SwitchCompanyMenu;

});
