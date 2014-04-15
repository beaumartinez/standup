# Standup

Have you ever been in a standup, and suddenly thought—

> What the FUCK did I do today?

I know I have. Hell, I think that every waking moment of my life.

Well, if you use [Codebase](http://www.codebasehq.com/) to manage your projects, boy are you in luck today.

## Installation

	pip3 install git+https://github.com/beaumartinez/standup.git

## Usage

To find out what the FUCK you did today, open up a terminal and type—

	standup_codebase.py -u<username> -k<key> <project>

(NB, you can find `<username>` and `<key>` in Codebase somewhere.) Wait a few seconds and BOOM instant standup information.

Type—

	standup_codebase.py -u<username> -k<key> <project> -a

And you can see what everyone else did as well, and call them out on LYING.

Lazy? Instead of typing your username and key everytime, you can create a JSON file at `~/.codebase`–

	{
		"username": "coolstorybro/beau",
		"key": "666"
	}

And then type—

	standup_codebase.py <project> -a

Much easier. Hit up `standup_codebase.py -h` for full help.

## License

I'm a pretty chill guy so I licensed this under the Do What The Fuck You Want Public License. So do what the FUCK you
want.
