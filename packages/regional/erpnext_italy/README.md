## ERPNext Italy

App to hold regional code for Italy, built on top of ERPNext.

### Introduction

ERPNext Italy aims to support regional customizations for Italy. The app is built on Frappe, a full-stack, meta-data driven, web framework, and integrates seamlessly with ERPNext, the most agile ERP software.

Some customizations include:
1. Italian E-invoicing -
This feature allows users to generate data from Sales Invoices and returns and then export generated data as XML (zipped for multiple invoices) for uploading to government portals.


2. Import supplier invoices -
ERPNext Italy has a feature to import supplier invoices from XML files provided by suppliers to the government. Using this you can import Supplier e-invoices into ERPNext. The supplier details like supplier names, addresses and purchase invoices will get created automatically in the system from the XML files.

### Installation

Using bench, [install ERPNext](https://github.com/frappe/bench#installation) as mentioned here.

Once ERPNext is installed, add ERPNext Italy app to your bench by running

```sh
$ bench get-app https://github.com/frappe/erpnext_italy.git
```

After that, you can install the app on required site (let's say demo.com )by running

```sh
$ bench --site demo.com install-app erpnext_italy
```

### License

GNU GPL V3. See [license.txt](https://github.com/frappe/erpnext_italy/blob/develop/license.txt) for more information.
