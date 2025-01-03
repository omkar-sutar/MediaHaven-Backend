# <u>MediaHaven API Server</u>

The MediaHaven API Server provides a simple and efficient way to manage and back up media content. Follow the steps below to configure and run the server.

---

## Usage

### Prerequisites:
- [Docker](https://docs.docker.com/) (optional but recommended)

### Step 1: Configure the Server ⚙️
1. Clone this repository and navigate to the project folder:

   ```bash
   git clone https://github.com/omkar-sutar/MediaHaven-Backend.git
   cd MediaHaven-Backend
   ```
2. **Create a `.env` file**

   ```bash
   vi .env
   ```

3. **Paste the following content into the `.env` file:**

   MediaHaven manages users and their credentials through environment variables. Add the desired users by including their usernames and passwords.

   ```text
   DATA_DIR=/data
   THUMBNAIL_DIR=.thumbnails
   SELF_PORT=5001

   # Users
   # Register user with username `USERNAME` and password `PASSWORD`
   # Username is case insensitive, while password is case sensitive.
   USER_USERNAME=PASSWORD
   ```

   **Description of environment variables:**
   
   - **`DATA_DIR`**: The container directory path where data will be stored.
   - **`THUMBNAIL_DIR`**: The directory inside `DATA_DIR` used to store thumbnails.
   - **`SELF_PORT`**: The port on which the server listens.
   - **`USER_USERNAME`**: Registers a user with the specified `USERNAME` (case insensitive) and `PASSWORD` (case sensitive).

   This configuration creates backup folders for the registered users in the `/data` directory. The `/data` directory is mapped to a host directory via Docker mounts.

4. **Build the Docker image** 🐋 (optional but recommended; find instructions [below](https://github.com/omkar-sutar/MediaHaven-Backend/blob/master/README.md#run-from-source) to run from source)

   ```bash
   ./docker_build.sh
   ```

---

### Step 2: Start the Server 🚀

Run the following command to start the server:

```bash
docker run -d -v "/host/dir:/data" \
--env-file .env \
-p 5001:5001 --name mediahavenbd mediahavenbd
```

> **Note:** Replace `/host/dir` with the actual directory path on the host system that will be used to store data.

You can also use the `docker_run.sh` script to perform the above operation. Ensure the script is edited to reflect your specific configuration.

### Run from source
To run from source, use 'run_from_source.sh`

---

### Verifying the Server

The server listens on `0.0.0.0:5001`. To verify that it is running, execute:

```bash
curl http://127.0.0.1:5001/ping
```

If the server is functioning correctly, it will respond to the `ping` request.

---

