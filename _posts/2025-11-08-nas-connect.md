---
title: 'Docker container setup inside synology nas'
date: 2025-11-07
permalink: /posts/docker-nas/
tags:
  - Synology
  - NAS
  - Docker
  - Globus
---



## From Terabytes to Analysis: Securely Connecting Your Synology NAS to HPRC with Globus and Docker

!['nas Image'](/images/nas-image.png)
Image generated in  Gemeni


So, you're like me. You have a *mountain* of data.

In my case, it was terabytes of video data from a recent project, all sitting comfortably on my local Synology NAS. This data wasn't just for show; it needed serious processing. And for serious processing, I needed the big guns: my university's High Performance Research Computing (HPRC) cluster.

This left me with a classic problem: How do I securely and efficiently move *terabytes* of data from my little NAS box to a massive HPC system?

This challenge took me the better part of a week to solve. I dove deep into the HPRC documentation, exploring data transfer methods. My requirements were strict:
1.  It had to be **secure**. I couldn't just open up ports (like FTP or SSH) on my NAS to the entire internet.
2.  It had to be **robust** and handle terabytes without failing.
3.  It had to be **compatible** with my Synology NAS.

The HPRC's preferred method, and the one that met all my criteria, was **Globus**. For a personal device like a NAS, the tool is **Globus Connect Personal**.

The only problem? Synology's DSM (its operating system) doesn't have a simple "click-to-install" package for Globus Connect Personal. The solution, it turned out, was **Docker**.

Here’s how I built a robust, secure data bridge from my NAS to the HPRC.

### The Solution: A Dockerized Globus Endpoint

The plan was simple: I would use Docker on my Synology NAS to run a lightweight Ubuntu container. Inside that container, I would manually install Globus Connect Personal. Then, I'd use Docker's "volumes" feature to mount my NAS data folder (e.g., `/volume1/dairy_file`) directly into the container.

This gives Globus access to the files without compromising the security of my NAS.

After a lot of trial and error, I landed on this `docker-compose.yml` file. It automates almost the entire setup.

```yaml
version: "3.8"

services:
  globusconnectpersonal:
    image: ubuntu:22.04
    container_name: globusconnectpersonal
    restart: unless-stopped

    # Mount your NAS data directory to the container
    # CHANGE THIS: Update "/volume1/dairy_file" to your actual NAS path
    volumes:
      - /volume1/dairy_file:/data

    environment:
      - TZ=America/Chicago

    entrypoint: >
      bash -c "
      echo 'Starting Globus Connect Personal setup...' &&
      apt-get update &&
      apt-get install -y wget tar sudo python3 &&
      
      # Create a non-root user 'globus'
      useradd -m -s /bin/bash globus &&
      echo '✅ User globus created.' &&
      
      # Download and extract Globus
      cd /home/globus &&
      wget -q [https://downloads.globus.org/globus-connect-personal/linux/stable/globusconnectpersonal-latest.tgz](https://downloads.globus.org/globus-connect-personal/linux/stable/globusconnectpersonal-latest.tgz) &&
      tar -xzf globusconnectpersonal-latest.tgz &&
      GLOBUS_DIR=$$(find . -type d -name 'globusconnectpersonal*' | head -n 1) &&
      
      # Set correct permissions for the new user
      chown -R globus:globus /home/globus /data &&
      echo '✅ Globus Connect Personal downloaded and permissions set.' &&
      echo '' &&
      
      # Print instructions for the human
      echo '---------------------------------------------------------------' &&
      echo '🚀 ACTION REQUIRED TO COMPLETE SETUP 🚀' &&
      echo '---------------------------------------------------------------' &&
      echo '1. Open a terminal into this container:' &&
      echo '   docker exec -it globusconnectpersonal bash' &&
      echo '' &&
      echo '2. Switch to the globus user:' &&
      echo '   su - globus' &&
      echo '' &&
      echo '3. Navigate to the Globus directory:' &&
      echo "   cd /home/globus/$${GLOBUS_DIR}" &&
      echo '' &&
      echo '4. Run the setup (get key from globus.org):' &&
      echo '   ./globusconnectpersonal -setup <YOUR_SETUP_KEY_HERE>' &&
      echo '' &&
      echo '5. After setup, start the endpoint:' &&
      echo '   ./globusconnectpersonal -start &' &&
      echo '' &&
      echo 'Your NAS folder is available at /data inside the container.' &&
      echo 'Container will keep running. Follow the steps above.' &&
      echo '---------------------------------------------------------------' &&
      
      # Keep the container alive
      tail -f /dev/null
      "
```



### 1. Save the File
Save the code above as `docker-compose.yml` in a folder on your Synology (e.g., in your `docker` shared folder).

### 2. Edit the Volume
Change `/volume1/dairy_file` to the exact path of the folder on your NAS that you want to share.  
`/data` is the name it will have inside the container, and you can leave that as-is.

### 3. Launch
Run:
```bash
docker-compose up -d
```
Or use the Synology Docker UI to launch the stack.

### 4. Get Your Key
Log in to the [Globus website](https://www.globus.org) and go to the **Endpoints** section.  
Click **Add a Personal Endpoint** and get the setup key.

---

## Configure the Container

1. Open an SSH terminal to your Synology NAS.
2. Get a terminal inside your new container:
   ```bash
   docker exec -it globusconnectpersonal bash
   ```
3. Follow the instructions printed in the container log (and in the entrypoint script above):
   ```bash
   su - globus
   cd /home/globus/globusconnectpersonal-*   # use tab-complete
   ./globusconnectpersonal -setup <PASTE_YOUR_KEY_HERE>
   ./globusconnectpersonal -start &
   ```

That’s it!  
If you go back to the Globus website, you’ll see your new endpoint is active.  
You can now browse the `/data` directory (which is your NAS folder) and initiate high-speed, secure transfers to your HPRC endpoint.

---

## ⚠️ Things to Watch Out For (The "Gotchas" I Learned)

This is the part that took me a week to figure out.

### ❌ You CANNOT Run as Root
Globus Connect Personal is designed to run as a **standard user**, not as root.  
My script explicitly creates a new user inside the container named `globus`.  
You **must** run:
```bash
su - globus
```
before you run the setup or start the service.  
If you try as root, it will fail.

### 🧑‍💻 The User "Myth"
I found a lot of conflicting documentation online claiming the user inside the container (e.g., `globus`) must match the user on your Synology NAS.  
This is **not true**.  
The Docker container is a completely isolated environment.  
The important part is that the `globus` user inside the container has **read/write permissions** on the mounted `/data` folder.  
My entrypoint script handles this with:
```bash
chown -R globus:globus /data
```

### 🔑 Permissions
The `chown` command is key — it gives the container’s `globus` user ownership of the `/data` mount point.  
This is what allows Globus to read your files.

---

It was a fantastic learning experience.  
I not only solved my data transfer problem but also got to deploy a container service that solves a real-world, practical issue.  
Hopefully, this guide saves you the week of troubleshooting it took me!
