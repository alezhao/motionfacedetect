# Motion Face Detect by Raspberry PI 4B

This lab is to introduce a solution regards use OpenCV 4 to detect and recognize person when motion detect happen. Application on Raspberry Pi 4b will send transaction message to Azure IOT HUB, then send notification to Microsoft Teams by Azure Logic App which trigger Azure Event Hub message from Azure IOT HUB.

![alt](images/oss_e2e.PNG)

#### Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).
- [Visual Studio Code](https://code.visualstudio.com/) on your machine with [Azure IoT Tools extension](https://marketplace.visualstudio.com/items?itemName=vsciot-vscode.azure-iot-tools).
- [Install Ubuntu 18.04 32bit GUI onto Raspberry Pi 4B](ubuntu/readme.md)
- [install Open CV4 onto Raspberry Pi 4B](opencv/readme.md)

#### Tutorials

- Configure Azure IOT HUB
- Configure Azure Event Hub 
- Configure Azure Logic App to trigger event hub message and route to **Microsoft Teams**
- Configure motion detect and facial recognition script onto Raspberry Pi 
- Verify