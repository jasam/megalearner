import argparse
import text_to_word
import classify_phonetic

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("action", help="words_in_dict | classify_phonetic")
	parser.add_argument("--input")
	parser.add_argument("--output")
	args = parser.parse_args()

	action = args.action
	input_arg = args.input
	output_arg = args.output

	if action == "words_in_dict":
		print("Reading source in: %s"%(input_arg))
		print("Output directory: %s"%(output_arg))
		text_to_word.main([input_arg, output_arg])

	elif action == "classify_phonetic":
		print("Reading source in: %s"%(input_arg))
		print("Output directory: %s"%(output_arg))
		classify_phonetic.main([input_arg, output_arg])

if __name__ == "__main__":
	main()