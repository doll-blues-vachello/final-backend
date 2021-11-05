# Backend task
Service is running at http://vezdekod.leadpogrommer.ru
### Uploading image
POST http://vezdekod.leadpogrommer.ru/upload
post parameter `file` - file you want to upload
### Download image
GET POST http://vezdekod.leadpogrommer.ru/get?id=<id>
optional parameter `scale`

### Testing with script
- Upload: `./testscript [--host hostname] upload file1 [file2 ...]`
- Download: `./testscript [--host hostname] get [--scale scale] id filename `

### Running
`docker-compose up --build`

### Images that aren't similar, but other db's might think that they ate the same
Look in `test-images` directory
