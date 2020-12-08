odoo.define('hodei_multi_company_header.inherit_header', function(require) {
'use strict';
var core = require('web.core');
var ajax = require('web.ajax');
var qweb = core.qweb;
ajax.loadXML('/hodei_multi_company_header/static/src/xml/header_view.xml', qweb);
});
