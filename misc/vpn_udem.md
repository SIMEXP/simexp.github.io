# UdeM VPN (Windows VM on Ubuntu)

## 🛠️ Part 1: Create a Clean Windows 10 VM (LTSC Recommended)

### 1. **Download Windows 10 LTSC (64-bit)**

* Visit: [https://archive.org/details/Windows10EnterpriseLTSC202164Bit](https://archive.org/details/Windows10EnterpriseLTSC202164Bit)
* Select **LTSC 2021**, 64-bit ISO
* Download and save the `.iso` to your `~/Downloads` folder

---

### 2. **Install VirtualBox**

```bash
sudo apt update
sudo apt install virtualbox
```

---

### 3. **Create the VM in Bash**

```bash
VM_NAME="WindowsVPN"
VM_DIR="$HOME/VirtualBox VMs/$VM_NAME"
ISO_PATH="$HOME/Downloads/your-downloaded-iso.iso"  # replace with real filename
DISK_SIZE=51200  # MB
RAM=4096
BRIDGE_ADAPTER=$(ip route | grep default | awk '{print $5}')

VBoxManage createvm --name "$VM_NAME" --ostype "Windows10_64" --register
VBoxManage modifyvm "$VM_NAME" \
  --memory $RAM --vram 128 \
  --boot1 dvd --graphicscontroller vmsvga \
  --nic1 bridged --bridgeadapter1 "$BRIDGE_ADAPTER" \
  --firmware efi

VBoxManage createhd --filename "$VM_DIR/$VM_NAME.vdi" --size $DISK_SIZE
VBoxManage storagectl "$VM_NAME" --name "SATA Controller" --add sata --controller IntelAhci
VBoxManage storageattach "$VM_NAME" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "$VM_DIR/$VM_NAME.vdi"
VBoxManage storageattach "$VM_NAME" --storagectl "SATA Controller" --port 1 --device 0 --type dvddrive --medium "$ISO_PATH"
VBoxManage startvm "$VM_NAME"
```
:::{tip}
If you get the following (scary) error when starting the VM:
```bash
VirtualBox can't enable the AMD-V extension. Please disable the KVM kernel extension, recompile your kernel and reboot (VERR_SVM_IN_USE)
```
Try to run the following instead of recompiling the kernel (!):
```bash
sudo modprobe -r kvm_amd
sudo modprobe -r kvm
```
:::

---

## 🪟 Part 2: Install and Configure Windows

### 4. **Install Windows**

* Go through the install steps
* Choose "I don’t have a product key"
* Select **Windows 10 Enterprise Evaluation**
* Skip updates and telemetry
* Log in and reach the desktop

---

### 5. **Install Guest Additions (Clipboard & Resolution Fixes)**

* In the VM: `Devices → Insert Guest Additions CD`
* Run the installer from File Explorer
* Reboot the VM

---

### 6. **Enable Copy-Paste Between Host and VM**

On Ubuntu:

```bash
VBoxManage controlvm "$VM_NAME" clipboard bidirectional
VBoxManage controlvm "$VM_NAME" draganddrop bidirectional
```

### 7. **Mouse auto-capture**

When you put your mouse on the virtual machine window it will auto-capture your mouse and you'll start interacting with the desktop inside the VM. There is a special key to toggle mouse autocapture on/off which will be handy to get back to ubuntu, resize the window or access other information. By default this key is the **right control key**, although it can be remapped through the VBOX interface.

## 🌐 Part 3: Install the UdeM VPN

### 8. Download Ivanti Secure Access VPN

In the VM, go to:

https://vpn.umontreal.ca/campus

Log in with your code d'accès and UNIP

Download the Ivanti Secure Access client for Windows

### 8. Install the VPN Client

Run the downloaded installer

Reboot if prompted

### 9. Configure the VPN

Open Ivanti Secure Access

Add a new connection:

Name: UdeM Campus

Server: https://vpn.umontreal.ca/campus

Save the profile

### 10. 🐧❤️ Profit! 

Activate the connection in the Ivanti Secure app, open FireFox and be ready to access all the wonderful UdeM online resources off campus, from the comfort of your Linux machine!

### 11. Keep on your toes!
It is very possible that Ivanti will push mandatory updates on you, and UdeM will not fail to double authenticate you constantly. Do not feel too comfortable. You can use VBOX to save a new snapshot of your virtual machine to save your progress in the menu Machine -> "take snapshot"
