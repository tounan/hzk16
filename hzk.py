#!/usr/bin/env python3

fd = open("HZK16/字库/16x16/hzk16s", "rb")
fontdata = fd.read()
fd.close()

def get_char(ch):
	encoded = ch.encode("gb2312")
	if len(encoded) == 2:
		v0, v1 = encoded
		offset = 94*(v0-0xa1)+(v1-0xa1)
		offset *= 32
	else:
		raise ValueError("Not GB2312")
	font = fontdata[offset: offset+32]

	out = ""
	# 32x8 to 16x16
	for k in range(16):
		for j in range(2):
			row = font[k*2+j]
			out += bin(row)[2:].zfill(8)
		out += "\n"
	return out

def chars_to_mif(chars, filename):
	outwords = []
	for char in chars:
		matrix = get_char(char).split("\n")
		for col in range(16):
			word = 0
			for row in range(16):
				word |= (int(matrix[row][col]) << row)
			outwords += [word]

	fd = open(filename, "wt")
	fd.write("""-- Copyright (C) 1991-2013 Altera Corporation
-- Your use of Altera Corporation's design tools, logic functions 
-- and other software and tools, and its AMPP partner logic 
-- functions, and any output files from any of the foregoing 
-- (including device programming or simulation files), and any 
-- associated documentation or information are expressly subject 
-- to the terms and conditions of the Altera Program License 
-- Subscription Agreement, Altera MegaCore Function License 
-- Agreement, or other applicable license agreement, including, 
-- without limitation, that your use is for the sole purpose of 
-- programming logic devices manufactured by Altera and sold by 
-- Altera or its authorized distributors.  Please refer to the 
-- applicable agreement for further details.

-- Quartus II generated Memory Initialization File (.mif)

WIDTH=16;
DEPTH=%d;

ADDRESS_RADIX=UNS;
DATA_RADIX=UNS;

CONTENT BEGIN
""" % len(outwords))
	for off, word in enumerate(outwords):
		fd.write("\t%d\t: %d;\n" % (off, word))
	fd.write("END;\n")
	fd.close()

if __name__ == "__main__":
	char = input("> ")
	print(get_char(char).replace("0", " ").replace("1", "*"))
	input("Press any key")
	
	#chars = "天雨粟鬼夜哭"
	#chars_to_mif(chars, "rom.mif")
