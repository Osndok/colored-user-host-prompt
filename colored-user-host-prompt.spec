
Name:           colored-user-host-prompt
Version:        0.0.2
Release:        1
Summary:        ANSI colored terminal prompts to help prevent sending the right commands to the wrong user or machine.

License:        GPLv2
URL:            http://github.com/Osndok/colored-user-host-prompt

BuildArch:      noarch

%description

Modifies the bash prompt (system-wide) such that both the user and host have distinct colors.

Heavily influenced by the following posts from the  community:
* http://superuser.com/questions/1123671/hash-hostname-into-a-color
* https://wiki.archlinux.org/index.php/Bash/Prompt_customization#Colors
* http://wiki.hackzine.org/development/misc/readline-color-prompt.html

%install
rm -rf $RPM_BUILD_ROOT
mkdir  $RPM_BUILD_ROOT
cd     $RPM_BUILD_ROOT

mkdir -p etc/profile.d

cat -> etc/profile.d/colored-user-host-prompt.sh <<"EOF"

# Skip this whole file for noninteractive shells.
[ -z "$PS1" ] && return

if [ "$UID" = "0" ]; then

# Short-circuit all the calls to other binaries & math for root, which should just be a bold/red prompt:
PS1='\[\e[1;31m\][\u \W]\$\[\e[0m\] '

else

TERM_COLORS=$(infocmp -1 | expand | sed -n -e "s/^ *colors#\([0-9][0-9]*\),.*/\1/p")
USERNAME_COLOR=$(echo $HOSTNAME $USER | sum | awk -v ncolors=$TERM_COLORS 'ncolors>1 {print 1 + ($1 % (ncolors - 1))}')
HOSTNAME_COLOR=$(hostname | sum | awk -v ncolors=$TERM_COLORS 'ncolors>1 {print 1 + ($1 % (ncolors - 1))}')
PS1_USER="\[$(tput setaf $USERNAME_COLOR)\]\u\[\e[m\]"
PS1_HOST="\[$(tput setaf $HOSTNAME_COLOR)\]\h\[\e[m\]"
PS1="[${PS1_USER}@${PS1_HOST} \W]\\$ "

fi

EOF


%files
%defattr(644,root,root)
/etc/profile.d/colored-user-host-prompt.sh


