# Deployment to Kubernetes

You can run the OpenEEW detection engine as a standalone Docker container on your laptop, a Rasberry Pi devices, or another computer. But you can also deploy it to a Kubernetes cluster such as the IBM Container Service or Red Hat OpenShift.

## Set up a Kubernetes cluster on the IBM Cloud

Register for an [IBM Cloud account](https://developer.ibm.com/dwwi/jsp/register.jsp?eventid=cfc-2020-projects), then set up a [free single worker node Kubernetes cluster](https://cloud.ibm.com/docs/containers?topic=containers-getting-started#clusters_gs).

Note: You can also choose a more scalable Kubernetes or OpenShift cluster, but those are not free.

* In the [IBM Cloud Catalog](https://cloud.ibm.com/catalog?category=containers), select **Kubernetes Service**. A cluster configuration page opens.
* From the plan dropdown, select the **Free** cluster option.
* Give your cluster a unique name, such as `openeew-free`.
* Select a resource group to create the cluster in, such as `default`.
* In the **Summary** pane, review the order summary and then click **Create**. A worker pool is created that contains one worker node in the default resource group.

While your cluster is provisioning, set up your local workstation with the client tools.

* Download and install a few CLI tools and the Kubernetes Service plug-in.

  ```shell-script
  curl -sL https://ibm.biz/idt-installer | bash
  ```

* Log in to your IBM Cloud account. Include the --sso option if you have a federated ID.

  ```shell-script
  ibmcloud login -a cloud.ibm.com -r us-south -g default
  ```

* Set the Kubernetes context to your cluster for this terminal session. This command will fail if the cluster isn't ready yet.

  ```shell-script
  ibmcloud ks cluster config --cluster <your cluster id>
  ```

* Verify that you can connect to your cluster.

  ```shell-script
  kubectl config current-context
  ```

* Now, you can run `kubectl` commands to manage your cluster on the IBM Cloud. For a full list of commands, see the [Kubernetes docs](https://kubectl.docs.kubernetes.io/).

## Run a deployment containing the Docker container

You can now deploy the `openeew/detector` app to your cluster.

* Select your cluster from the [cluster list](https://cloud.ibm.com/kubernetes/clusters) to open the details for your cluster.
* Click **Kubernetes dashboard**.
* From the menu bar, click the **Create new resource** icon (+).
* Select the **Create from form** tab.
  * Enter a name for your app, such as `openeew`.
  * Enter `openeew/detector` for your container image.
  * Enter the number of pods for your app deployment, such as `1`.
  * Leave the **Service** drop-down menu set to **None**.
  * Click **Show advanced options** and add environment variables for `username` and `password`
* Click **Deploy**. During the deployment, the cluster downloads the `openeew/detector` container image from Docker Hub and deploys the app in your cluster.
* Create a node port so that your app can be access by other users internally or externally. Because your cluster is a free cluster, you can only expose an app with a node port, not a load balancer or Ingress.
  * Click the **Create new resource** icon (+).
  * Copy the [node port YAML](openeew.yaml).
  * In the **Create from input** box, paste the node port YAML that you copied in the previous step.
  * Click **Upload**. The node port service is created.
* From the menu, click Service > Services, and note the TCP endpoint port of your liberty service in the node port range 30000 - 32767, such as openeew:31883 TCP.
* From the menu, click Workloads > Pods, and note the Node that your pod runs on, such as 10.xxx.xx.xxx.
* Return to the IBM Cloud clusters console, select your cluster, and click the Worker Nodes tab. Find the Public IP of the worker node that matches the private IP of the node that the pod runs on. Save this IP for the next step

## Simulate messages

From your local workstation, run the simulator script:

```shell-script
cd openeew
python3 sensor_simulator.py \
--username admin \
--password admin \
--earthquake 2018_7.2 \
--port 31883 \
--host <your public IP from above>
```

The simulator will now send one reading per second per simulated sensor.

## Monitoring the data flowing through the system

In the Kubernetes dashboard, select **Pods** and find the "Logs" menu under the three dots at the far right of the `openeew` pod. You can also `exec` into the running container to explore other logs under `/var/log`.

You can also now use any of the other dashboard or `kubectl` command line functions to manage your detector engine.

## Next steps

If you'd like to contribute to creating a distributed system on Kubernetes with a separate MQTT system, separate PostgreSQL database, and separate dashboard web app, please open an issue or submit a pull request. 

We are also interested in documenting how to create a system based on the Watson IoT Platform, PostgreSQL databases for Compose, and a dashboard run as a Cloud Foundry or Kubernetes web application.
