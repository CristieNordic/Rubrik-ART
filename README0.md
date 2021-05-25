# Nextcloud for OpenShift 4.x with Cloudian HyperStore

This repository contains an OpenShift 4 template to easily deploy Nextcloud with MariaDB on OpenShift  using Cloudian HyperStore S3 Storage.

## Installation

### 0 Create OpenShift project

Create an OpenShift project if not already provided by the service

```
PROJECT=nextcloud
oc new-project $PROJECT
```

### 1 Deploy Nextcloud

```
oc process -f https://raw.githubusercontent.com/CristieNordic/nextcloud-openshift/master/nextcloud.yaml -p NEXTCLOUD_HOST=<url that will be exposed> -p S3_BUCKET=<Bucket Name> -p S3_HOST=<url to your S3 target> -p S3_ACCESS_KEY=<your access key> -p S3_SECRET_KEY=<your secret key> |oc create -f -
```

#### Template parameters

Execute the following command to get the available parameters:

```
oc process -f https://raw.githubusercontent.com/CristieNordic/nextcloud-openshift/master/nextcloud.yaml --parameters
```

### 2 Configure Nextcloud

* Navigate to http://nextcloud.example.com
* Fill in the form and finish the installation.

**Hints**

* You might want to enable TLS for your instance

## Backup

### Database
We recommend to use [Cristie Backup Solution](https://www.cristienordic.com/data-protection) where you have Container Backup Support.

## Notes

* Nextcloud Cronjob is called from a `CronJob` object every 15 minutes
* The S3 functionality in this package should work fine also with IBM Cloud Object Storage and not only Amazon AWS S3 or Cloudian HyperStore.

To use the `occ` CLI, you can use `oc exec`:

```
oc get pods
oc exec NEXTCLOUDPOD -c nextcloud -ti php occ
```

## Know Issues

* When applying NextCloud on slow storage it can end up with a `504 Gateway Timeout` error. Refresh the page and the configuration will finish.
If you want to solve this here is a blog that explains what you need to do [Blog](https://mamchenkov.net/wordpress/2016/08/04/504-gateway-timeout-error-on-nginx-fastcgi-php-fpm/)
* If you are using Self Signed Certificate on a Cloudian, you cannot run over `https` and port `443`. You most run over port `80` and using `-p S3_SSL=false`

## Contributions

Very welcome!

1. Fork it (https://github.com/CristieNordic/nextcloud-openshift/fork)
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request
