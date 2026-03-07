# Application Security Project

Writeup can be found [here](https://gtinfosec.org/projects/pr1.html).

### Getting Started

Start by running `./build.sh` to set up your targets. It will prompt 
for GT usernames (e.g., gburdell3). Enter all GT usernames in your group, separated by spaces.
Each group’s targets will be slightly different, so make sure your
GT usernames are correct!

Your `./build.sh` output should look like this:
```
$ ./build.sh 
Enter the GT usernames of all the members in your team, separated by spaces - ytan328 pnarasimhan33 rluo47
Using cookie for ['pnarasimhan33@gatech.edu', 'rluo47@gatech.edu', 'ytan328@gatech.edu']
Setup complete.
```

### Testing

We've provided `test.sh` to help check that your solutions match
the spec. However, this script is not the autograder, and it is not
authoritative. The spec (and autograder) has a few requirements beyond
what the script verifies, and it's up to you to test carefully.
