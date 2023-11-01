# Installation

```bash
wget https://raw.githubusercontent.com/ZorionTen/TheChat/main/client/install
chmod +x install
./install
```

# BUILD INSTRUCTIONS
### Just for reference. do not use
### Buildiding binary is not recommended. updates will fail if using binary
### Clone the main branch, then in the `TheChat/client` run  
```bash
pyinstaller --onefile ./client.py --add-data 'views:views'
```
