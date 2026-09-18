Status: Source
Relocated: Consolidated linear outline: `../../ai-docs/boot-sequence-linear.md` (Additional extractions previously referenced remain pending creation.)

The boot sequence handles the initial loadout for the entire base operating layer, its allowed accesses and any additional core parameters to write.

As this virtual, there is no disk boot or CPU protected mode stuff. This entire _boot_ layer reads a "bios" of base configurations for identity strings and base settings for the vol env.

The VOL will exist on a device within its own environment and will need its own platform to work upon.
Initially python - this entire build-out will become assembly but the process will remain. It'll remain independent of the suite/kernel/BIOS.

## 1. process foreign boot

 The startup for this script will be a console process initiating the mandatory loadout. Essentially pressing the 'on' switch. It's unlikely any parameters will exist, owning to the SYSTEM implemented call procedure - they will probably be an init file - but this should be burnt into the boot sequence.

## 2. load boot sem

 The self executing module provides all required parameters to chain the next offloaded event; master boot record. As a ZIM-SEM it'll assign its own parameters for load.

 The boot zim sem is pre-compiled for the target platform. It maintains the GUID and init settings for readout. The intial statement will execute a store using SEM TAPE into a new memory reference (mcom). The mcom file descriptor is anonymous, containing the loading step values as a TAPE string.

 And additional environment parameters preload the working env and the VOL BIOD dies; executing into its own process.

 At this point the basic virtual environment is installed for the bios - potentially on another thread.

 And continuing statements load until the bios emits a complete to the parent (this) boot manager.

## 3. MBR

 The Master boot record doesn't exist. In this analogy it defines the first unprotected configurable point for starting a VOL. The env is fully prepared and the config and kernel address are written to an mcom TAPE location by the boot sem.

 The MBR in this case is another sem responsible for accepting the BIOS configuration, reading the values and managing a control pass to a chosen kernel.

 At this point all _hardware_, _drivers_ and _software_ platform should prepare. Being virtual this is the initial libraries to start allowed IO's/APIs and address any initial kernel requirements - such as a basic VDU.

 All driven components are built into the driver selection access by the MBR.

 In a windows env, this will open the write DB, allocate threads, maintain a basic connection to peripherals and start utilize the CMD std in out.

 An example such as linux pi device. This core boot is again python based access of device drivers; turning on e-ink screens and finding the right inputs and outputs goverened by the drivers.
 The drivers will be a combination of libs and system APIs to bridge the VOL for all operating system usage.

 In a VOL container (the CEF with embedded python, assembly assets and c based extras) the IO is _transparent_ with sibling threads monitoring peripherals for events.

## Drivers.

The hardware layer for all target devices will differ - drivers are a combination of libs and external accesses.

+ I-pod/i-pad (not native)
+ pi-device
+ windows/linux

Primarily the i-device platform is for visual rendering and is considered a passive device. If deploying a boot process it can be done through non native - container  platforms of python or another bridged language (transpiled). Deploying using python shouldn't cater much effort as platforms exist for this.

The hardware layer will consist of a cleaner API to already existing APIS for components.

In other areas; android or any linux base is a target platform. Hardware drivers are native or lib native.

---

The MBR maintains a compiled startup of assets to load - As the system assets may not exist; the mbar will map accordingly.

This is all relatively low-level. As after a kernel has implemented the visual application layer, a standardaised API for any base output will exist.

In example the _VDU_ may be one or many of:

+ Actual monitor on a PC will low-level access
+ CLI only
+ 3D space VR
+ Any other WEBGL printout
+ Pi Mini displays, e-ink, custom oled screens
+ remote socket (VNC)
+ X-Display

... Should all have a `text out()` statement...
