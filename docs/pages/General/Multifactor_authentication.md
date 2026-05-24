---
title: "Multifactor authentication/en"
url: "https://docs.alliancecan.ca/wiki/Multifactor_authentication/en"
category: "General"
last_modified: "2026-05-13T14:50:01Z"
page_id: 22441
display_title: "Multifactor authentication"
---

Multifactor authentication (MFA) allows you to protect your account with more than a password. Once your account is configured to use this feature, you will need to enter your username and password as usual, and then perform a second action (the second factor) to access most of our services.

You can choose any of these factors for this second authentication step:
*Approve a notification on a smart device through the Duo Mobile application.
*Enter a code generated on demand.
*Push a button on a hardware key (YubiKey).

This feature will be gradually deployed and will not be immediately available for all of our services.

= Recorded webinars =
Two webinars were presented in October 2023. Their recordings are available here:
* Authentification multifacteur pour la communauté de recherche (French)
* Multifactor authentication for researchers (English)

= Registering factors =
== Registering multiple factors ==
When you enable multifactor authentication for your account, we strongly recommend that you configure at least two options for your second factor. For example, you can use a phone and single-use codes; a phone and a hardware key; or two hardware keys. This will ensure that if you lose one factor, you can still use your other one to access your account.

== Use a smartphone or tablet ==

#Install the Duo Mobile authentication application from the Apple Store or Google Play. Make sure to get the correct application (see icon below). TOTP applications such as Aegis, Google Authenticator, and Microsoft Authenticator are not compatible with Duo and will not scan the QR code.
#Go to the CCDB, log in to your account and select My account → Multifactor authentication management.
#Under Register a device, click on Duo Mobile.
#Enter a name for your device. Click on Continue. A QR code will be displayed.
#In the Duo Mobile application, tap Set up account or the “+” sign.
#Tap Use a QR code.
#Scan the QR code shown to you in CCDB. Important: Make sure that your mobile device is connected to the internet (over wi-fi or cellular data) while you are scanning the QR code.

File:Duo-mobile-app-icon.png|Step 1
File:Duo-mobile-option-en.png|Step 3
File:Naming-duo-mobile-device-en.png|Step 4
File:Duo-mobile-add-account.png|Step 5
File:Duo-mobile-scan-qr-code.png|Step 6
File:Scanning-CCDB-QR-code.jpg|Step 7

== Use a YubiKey ==
A YubiKey is a small hardware token made by the Yubico company. If you do not wish to use your phone or tablet for multifactor authentication, do not have a smartphone or tablet that supports Duo, or are often in a situation when using your phone or tablet is not possible, then a YubiKey is your best option.  Different YubiKey models can fit in USB-A, USB-C, or Lightning ports, and some also support near-field communication (NFC) for use with a phone or tablet.

A YubiKey must support the "Yubico OTP" function to work with our systems.
We recommend using the YubiKey 5 Series, but older or newer devices may also work.
See this Yubico identification page to determine whether a specific product offers the function "Yubico OTP".

If you register a YubiKey for multifactor authentication, when you log on to one of our clusters you will be prompted for a one-time password (OTP)---
although the prompt may use different terminology such as "Enter a passcode".
You respond by touching a button on your YubiKey, which generates a string of characters to complete your authentication.
Using a YubiKey does not require any typing on the keyboard: the YubiKey connected to your computer “types” the string when you touch its button.

To register a YubiKey you will need its Public ID, Private ID, and Secret Key.
If you have this information, go to the Multifactor authentication management page.
If you do not have this information, configure your key using the steps below.

=== Configuring your YubiKey for Yubico OTP ===

# If you use a pop-up blocker, disable it because some of the following steps involve pop-up windows
# Download and install the YubiKey Authenticator application from the Yubico website.
# Insert your YubiKey and launch the YubiKey Authenticator software.
# In YubiKey Authenticator, select Slots.  (Images below illustrate this and the next few steps.)
# Select either slot 1 or slot 2. Slot 1 corresponds to a short touch (pressing for 1 to 2.5 seconds), while slot 2 is a long touch on the key (pressing for 3 to 5 seconds). Slot 1 is typically pre-registered for Yubico cloud mode. If you are already using this slot for other services, either use slot 2, or click on Swap slots to transfer the configuration to slot 2 before configuring slot 1.
# Select Yubico OTP / Program a Yubico OTP credential.
# In the "Public ID" field click Use serial, then generate a Private ID and a Secret key. Securely save a copy of the data in the Public ID, Private ID, and Secret key fields, as you will need them shortly.
# IMPORTANT: Click on "Save".
# Log into the CCDB to register your YubiKey in the Multifactor authentication management page.

File:Yubico-Authenticator-Step3.png|Step 3
File:Yubico-Authenticator-Step4.png|Step 4, Step 5
File:Yubico-Authenticator-Step6.png|Step 6
File:Yubico-Authenticator-Step7.png|Step 7
CCDB Yubikeys.png|Step 8

You can test your Yubikey setup by pressing the button on it any time while it is inserted into your computer.  If set up correctly, it should generate a code at your prompt or cursor.

= Using your second factor =
== When connecting via SSH ==
When you connect to a cluster using SSH, you will be prompted for your second factor after you first supply either your password or your SSH key. This prompt will look like this:

At this point, you can select which phone or tablet you want Duo to send a notification to. If you have multiple devices enrolled, you will be shown a list. You will then get a notification on your device, which you accept to complete the authentication.

If you are using a YubiKey, simply touch the YubiKey when the "Passcode" prompt appears.
If you are using a backup code or a time-based one-time password that the Duo Mobile application shows, you will have to paste it or type it at the prompt.

=== Configuring your SSH client with ControlMaster ===

==== Linux and MacOS ====
If you use OpenSSH to connect, you can reduce how frequently you are asked for a second factor. To do so, edit your .ssh/config to add the lines:

Host HOSTNAME
    ControlPath ~/.ssh/cm-%r@%h:%p
    ControlMaster auto
    ControlPersist 10m

where you would replace HOSTNAME with the host name of the server for which you want this configuration.  This setting allows a first SSH session to ask for the first and second factors, but subsequent SSH connections on the same device will reuse the connection of the first session (without asking for authentication), even up to 10 minutes after that first session was disconnected.

Note that the above ControlMaster mechanism (a.k.a. Multiplexing) doesn't work with native Windows, in which case Windows Subsystem for Linux will be required. See the link below.

====Windows ====

See Configuring WSL as a ControlMaster relay server.

== When authenticating to our account portal ==
Once multifactor authentication is enabled on your account, you will be required to use it when connecting to our account portal. After entering your username and password, you will see a prompt similar to this, where you click on the option you want to use.
(Note: This screen will be updated.)

File:CCDB MFA prompt.png

= Configuring common SSH clients =
Command line clients will typically support multifactor authentication without additional configuration. This is however often not the case for all clients. Below are instructions specific to a few of them.

== FileZilla ==
FileZilla will ask the password and second factor each time a transfer is initiated because by default, transfers use independent connections which are closed automatically after some idle time.

To avoid entering the password and second factor multiple times, you can limit the number of connections to each site to “1” in “Site Manager” => “Transfer Settings tab”; note that you’ll then lose the ability to browse the server during transfers.

# Launch FileZilla and select “Site Manager”
# From the “Site Manager”, create a new site (or edit an existing one)
# On the “General” tab, specify the following:
#* Protocol: “SFTP – SSH File Transfer Protocol”
#* Host: [the cluster login hostname]
#* Logon Type: “Interactive”
#* User: [your username]
# On the “Transfer Settings” tab, specify the following:
#* Limit number of simultaneous connections: [checked]
#* Maximum number of connections: 1
# Select “OK” to save the connection
# Test the connection

=== Niagara special case ===
Connections in FileZilla can only be configured to use either SSH keys or interactive prompts, not both. Since Niagara requires using SSH keys and an MFA prompt, using FileZilla is challenging. We recommend using a different SCP client that has better support for interactive prompt, but one possible way to work around is to:

# Attempt to connect with an SSH key. This will fail because of the interactive prompt for the second factor. FileZilla will then remember your key.
# Change the login method to interactive and attempt to connect again. You will then receive the 2FA prompt.

== MobaXTerm ==
Install version 23.1 or later.
Version 23.5 (on Archive.org) is the latest version for which the following instructions work for most users.

==== Prompt on file transfer ====

When connecting to a remote server, MobaXterm establishes two connections by default:
the first for the terminal and the second for the remote file browser.
By default, the file browser uses the SFTP protocol,
which causes a mandatory second prompt for your second factor of authentication.

This behaviour can be improved by switching the SSH-browser type to
"SCP (enhanced speed)" or "SCP (normal speed)" in the session's Advanced SSH settings.

==== Use SSH key instead of password ====

To resolve the following issues (1) allow downloads and (2) use SSH passphrase instead of Digital Research Alliance of Canada password, make the following changes to SSH settings (SSH tab in Settings dialogue):

Uncheck "GSSAPI Kerberos"
Uncheck "Use external Pageant"
Check "Use internal SSH agent "MobAgent""
Use the "+" button to select SSH key file.

==== Known issues with MFA ====
We noticed that after adoption of MFA, MobaXTerm presents a strange behavior, more or less prevalent depending on the version. Although files can be opened via the terminal, when you try to open, download, or upload files using the navigation bar on the left, operations hang indefinitely.

Basically there are pretty much 3 independent sessions that need to be initiated and authenticated when you use MobaXterm:

to open the ssh terminal
to display the contents of the folder on the left pane
to start the transfer of files

It's possible that 1 or 2 hidden MFA-Duo windows (behind other windows) on your computer are waiting for authentication.

In addition, each time you navigate to a different folder on the left pane, another transaction requiring MFA is started. Some versions of MobaXterm handle this better than others.

== PuTTY ==
Install version 0.72 or later.

== WinSCP ==
Ensure that you are using SSH Keys.

== PyCharm ==
In order to connect to our clusters with PyCharm, you must setup your SSH Keys before connecting.

When you connect to a remote host in PyCharm, enter your username and the host you want to connect to. You will then be asked to enter a "One time password" during the authentication process. At this stage, use either your YubiKey or your generated password in Duo, depending on what you have setup in your account.

== Cyberduck ==
By default, Cyberduck opens a new connection for every file transfer, prompting you for your second factor each time. To change this, go in the application's preferences, under Transfers, in the General section, use the drop-down menu beside the Transfer Files item and select Use browser connection.

Then, ensure that the box beside Segmented downloads with multiple connections per file is not checked. It should look like the picture below.

= Frequently asked questions =
== Can I use Authy/Google authenticator/Microsoft Authenticator ? ==
No. Only Duo Mobile will work.

== I do not have a smartphone or tablet, and I do not want to buy a Yubikey ==
Unfortunately, that means you cannot use our services. Multifactor authentication is mandatory. A Yubikey hardware token is the cheapest way to enable multifactor authentication on your account, and is expected to be covered by the principal investigator's research funding like any other work-related hardware. Mandating multifactor authentication is a requirement from our funding bodies.

== Why can't you send me one time passcodes through SMS ? ==
Sending SMS costs money which we do not have. Multifactor using SMS is also widely regarded as insecure by most security experts.

== Why can't you send me one time passcodes through email ? ==
No, Duo does not support sending one time code through email.

== I have an older Android phone and I cannot download the Duo Mobile application from the Google Play site. Can I still use Duo ? ==

Duo Mobile is only available for Android versions that receive security updates. While you might be able to download and install it manually on older Android versions by following these instructions, the application might not work properly or at all, and the Duo service might reject authentication attempts.

== I want to disable multifactor authentication. How do I do this? ==
Multifactor authentication is mandatory.  Users cannot disable it. Exceptions can only be granted for automation purposes. If you find that multifactor authentication is annoying, we recommend applying one of the configurations listed above, depending on the SSH client you are using. Our recorded webinars also contain many tips on how to make MFA less burdensome to use.

== I do not have a smartphone or tablet, or they are too old. Can I still use multifactor authentication? ==
Yes. In this case, you need to use a YubiKey.

== I have lost my second factor device. What can I do? ==
* If you have bypass codes, or if you have more than one registered device, use one of these other mechanisms to connect to your account on our portal. If you have a new device, register it then. Finally, delete your lost device. Note that you cannot delete a device if it is the only one registered.
* If you do not have bypass codes and have lost all of your registered devices, copy the following list providing answers to as many questions as you can. Email this information to support@tech.alliancecan.ca.

  What is the primary email address registered in your account?
  For how long have you had an active account with us?
  What is your research area?
  What is your IP address? (to see your IP address, point your browser to this link).
  Who is the principal investigator sponsoring your account?
  Who are your group members?
  Whom can we contact to validate your request?
  Which clusters do you use the most?
  Which software modules do you load most often on the clusters?
  When did you run your last job on the clusters?
  Provide a few of your latest batch job IDs on the clusters.
  Provide ticket topics and ticket IDs from your recent requests for technical support.

== Which SSH clients can be used when multifactor authentication is configured? ==
* Most clients that use a command-line interface, such as on Linux and Mac OS.
* Cyberduck
* FileZilla
* JuiceSSH on Android
* MobaXTerm
* PuTTY
* PyCharm
* Termius on iOS
* VSCode
* WinSCP

== I need to have automated SSH connections to the clusters through my account. Can I use multifactor authentication ? ==
We are currently deploying a set of login nodes dedicated to automated processes that require unattended SSH connections. More information about this can be found here.

== Why have I received the message "Access denied. Duo Security does not provide services in your current location" ? ==
Duo blocks authentications from users whose IP address originates in a country or a region subject to economic and trade sanctions: Duo help.

= Advanced usage =
== Configuring your YubiKey for Yubico OTP using the Command Line (ykman)==
# Install the command line YubiKey Manager software (ykman) following instructions for your OS from Yubico's ykman guide.
# Insert your YubiKey and read key information with the command ykman info.
# Read OTP information with the command ykman otp info.
# Select the slot you wish to program and use the command ykman otp yubiotp to program it.
# Securely save a copy of the data in the Public ID, Private ID, and Secret Key fields. You will need the data for the next step.
# Log into the CCDB to register your YubiKey in the Multifactor authentication management page.

:
[name@yourLaptop]$ ykman otp yubiotp -uGgP vvcccctffclk 2
Using a randomly generated private ID: bc3dd98eaa12
Using a randomly generated secret key: ae012f11bc5a00d3cac00f1d57aa0b12
Upload credential to YubiCloud? [y/N]: y
Upload to YubiCloud initiated successfully.
Program an OTP credential in slot 2? [y/N]: y
Opening upload form in browser: https://upload.yubico.com/proceed/4567ad02-c3a2-1234-a1c3-abe3f4d21c69