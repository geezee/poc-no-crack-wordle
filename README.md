# Proof-of-Concept Wordle

This is a proof of concept that Wordle can be implemented in such a way that only a brute-force
dictionary attack is possible with minimal work from the server.

I am hosting a running example on my [website](https://grgz.me/wordle) which
generates a new word every hour.

For more information on the concepts behind it, read my blog post
[A harder-to-crack Wordle](https://blog.grgz.me/posts/crack-wordle.html)

The code is split in two folders:

- The `server/` folder contains the files needed to be executed on the server.
The python script will read the `dict.txt` file, so it's essential that they remain together in the same folder.
oreover the script produces a `data.bin` file which is a binary encoding of the generated table.
The python script is documented, so read the comments.

- The `client/` folder contains the files that should be exposed in the web server.

To encourage attempts at breaking the game, without use of brute-force dictionary attacks, no code is obfuscated or made ugly.
And only the minimum number of features are implemented.

The client logic is in 160 lines of vanilla Javascript, and the server logic is in 125 lines of documented Python3 code.


# Deployment

There's a handy `setup.sh` executable with two environment variables `APP_PATH`, and `PYTHON3`.
You should assign to `APP_PATH` the full path of the cloned repository, and to `PYTHON3` the full path of the python3 executable.

If you choose to scatter the `server` and `client` folders you will need to adapt the script.

There will be logs written to `server/server.log` that is just the output of the generation script.


## Crontab

I use the following cron expression:

```
0 */1 * * * /path/to/app/setup.sh
```


# License

This code is licensed under GPLv3.
