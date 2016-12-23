#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import lxc
import shutil
#import sys
import subprocess
import tarfile

def copy_container(work_directory,name):
	path = work_directory + name
	print(path)
	backup_path = backup_directory + name
	print(backup_path)
	#shutil.copyfileobj(path,backup_path)
	subprocess.call(["cp","-R",path,backup_path])

def archive_container(backup_directory,name):
	print("Archiving file")
	print("................")
	backup_path = backup_directory + name
	tar = tarfile.open(backup_path + ".tar.gz", "w:gz")
	tar.add(backup_path, arcname = backup_path)
	tar.close()
	print("DONE create archive")

def remove_container_directory(backup_directory,name):
	destroy_directory = backup_directory + name
	shutil.rmtree(destroy_directory)

work_directory = "/var/lib/lxc/"
#backup_directory = "/srv/photo_backup/"
backup_directory = "/srv/"

array_container = lxc.list_containers()
for i in array_container:
	print(work_directory + i)
	print(lxc.Container(i).state)
	if lxc.Container(i).state != 'STOPPED':
		lxc.Container(i).freeze()
		print(i + " " + lxc.Container(i).state)
		print("COPY")
		copy_container(work_directory,i)
		print("...................")
		lxc.Container(i).unfreeze()
		print("UNFREEZING")
		print(i + " " + lxc.Container(i).state)
	else:
		print("COPY STOPPED CONTAINER")
		copy_container(work_directory,i)
	archive_container(backup_directory,i)
	remove_container_directory(backup_directory,i)

