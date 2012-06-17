#ENQUEUE

ENQUEUEIMAGE_POST="enqueueimage.post.count_"
ENQUEUEIMAGE_OK="enqueueimage.success.count_"
ENQUEUEIMAGE_FAILURE="enqueueimage.fail.count_"

#ESSENTIAL
IMGPROCESSING_GET="imageprocessing.get.count_"   # number of GET requests
IMGPROCESSING_POST="imageprocessing.post.count_"   # number of POST request
IMGPROCESSING_FAILURE="imageprocessing.fail.count_" # request processing failed
IMGPROCESSING_OK="imageprocessing.success.count_"   # request successfully passed
IMGPROCESSING_PROCESSTIME="imageprocessing.process.time_"   # request successfully passed
IMGPROCESSING_FAILURE_GIVEUP="imageprocessing.fail.giveup_" # the return code of download

#DOWNLOAD
IMGPROCESSING_DOWNLOADCOUNT="imageprocessing.download.count" # the total download time
IMGPROCESSING_DOWNLOADTIME="imageprocessing.download.time" # the total download time
IMGPROCESSING_DOWNLOADBYTE="imageprocessing.download.byte" # the total byte download
IMGPROCESSING_DOWNLOADRETCODE="imageprocessing.download.returncode_" # the return code of download



#STORAGE interaction
IMGPROCESSING_S3="imageprocessing.s3.uploadcount" # the number of files uploaded to S3
IMGPROCESSING_GS="imageprocessing.gs.uploadcount" # the number of files uploaded in GS

IMGPROCESSING_TOTAL_BYTEUPLOAD="imageprocessing.cloud.uploadbytecount" # the number bytes successfully upload to cloud
IMGPROCESSING_TOTAL_TIMEUPLOAD="imageprocessing.could.uploadtime" # the return code of download
IMGPROCESSING_TOTAL_COUNTUPLOAD="imageprocessing.cloud.uploadcount" # the number times successfully upload to cloud
#CONVERSION

IMGPROCESSING_CONVERSIONTIME="imageprocessing.convertsion.time" # number of image conversion
IMGPROCESSING_CONVERSIONCOUNT="imageprocessing.convertsion.count" # the time spend on image conversion (without cloud upload)



