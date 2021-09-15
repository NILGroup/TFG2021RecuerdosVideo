from post_procesar_transcripcion import divide_by_speaker, split_by_sections
from summarizer import summarize_array, generate_summary


def summarize(transcript, is_diarized, divide_by_speaker_option, divide_by_segments_option, size_segments):
  summary=""
  if(divide_by_speaker_option):
    spkr1, spkr2 = divide_by_speaker(transcript)
    text_array=[spkr1, spkr2]
    if(divide_by_segments_option):
      result=[]
      for text in text_array:
        text_sections = split_by_sections(text, size_segments)
        result.append(text_sections)
      text_array= result
      i=1
      result=[]
      for speaker in text_array:
        result.append("---------------- " + str(i) + " ---------------\n" + summarize_array(speaker))
        i=i+1
      text_array=result
      summary =  "\n".join((item for item in text_array))
    else:
      i=1
      result=[]
      for speaker in text_array:
        result.append("---------------- " + str(i) + " ---------------\n" + generate_summary(speaker))
        i=i+1
        text_array=result
        summary =  "\n".join((item for item in text_array))
  else:
    if(is_diarized): transcript="\n".join(item for item in map(lambda e: e[2:],transcript.splitlines()))
    if(divide_by_segments_option):
      summary = summarize_array(split_by_sections(transcript, size_segments))
    else:
      summary= generate_summary(transcript)
  return summary