#include "cJSON.h"
int stream_save_encode_result(MGVL1_CAPTURE_RESULT_S *result, int width, int height)
{
	int ret = MGVL1_RET_ERROR;
	int i = 0;
	cJSON *request_obj = NULL;
	cJSON *meta_item = NULL;
	cJSON *detect_list_array = NULL;
	cJSON *extra_list_array = NULL;
    char * json_print = NULL;

	DEBUG("############## in mgvl1_encode_message ################ !!!\n");

	if(!result)
	{
		DEBUG( "input param is NULL !!!\n");
		ret = MGVL1_RET_ERROR;
		goto EXIT;
	}

	request_obj = cJSON_CreateObject();
	meta_item = cJSON_CreateObject();
	cJSON_AddNumberToObject(meta_item, "frame_id", result->frame_id);
	cJSON_AddNumberToObject(meta_item, "width", width);
	cJSON_AddNumberToObject(meta_item, "height", height);
	cJSON_AddItemToObject(request_obj, "meta", meta_item);

	//检测框信息
	detect_list_array = cJSON_CreateArray();
	for(i = 0; i < result->face_list_size; i++)
	{
		cJSON* detect_item = cJSON_CreateObject();
		cJSON_AddNumberToObject(detect_item, "frame_id", result->face_list[i].frame_id);
		cJSON_AddNumberToObject(detect_item, "track_id", result->face_list[i].track_id);
		cJSON_AddNumberToObject(detect_item, "left", result->face_list[i].rect.left);
		cJSON_AddNumberToObject(detect_item, "right", result->face_list[i].rect.right);
		cJSON_AddNumberToObject(detect_item, "top", result->face_list[i].rect.top);
		cJSON_AddNumberToObject(detect_item, "bottom", result->face_list[i].rect.bottom);
		
		cJSON* info_item = cJSON_CreateObject();
		cJSON_AddNumberToObject(info_item, "roll", result->face_list[i].pose.roll);
		cJSON_AddNumberToObject(info_item, "pitch", result->face_list[i].pose.pitch);
		cJSON_AddNumberToObject(info_item, "yaw", result->face_list[i].pose.yaw);
		cJSON_AddNumberToObject(info_item, "blur", result->face_list[i].blur);
		cJSON_AddItemToObject(detect_item, "info", info_item);

		//@ 可选的信息
		#if 0
		//设置框的颜色
		cJSON* color_item = cJSON_CreateObject();
		cJSON_AddNumberToObject(color_item, "b", 255);
		cJSON_AddNumberToObject(color_item, "g", 0);
		cJSON_AddNumberToObject(color_item, "r", 0);
		cJSON_AddItemToObject(detect_item, "color", color_item);
		#endif
		
		cJSON_AddItemToArray(detect_list_array, detect_item);
	}
	cJSON_AddItemToObject(request_obj, "detect", detect_list_array);

	//推图框信息
	extra_list_array = cJSON_CreateArray();
	for(i = 0; i < result->feature_list_size; i++)
	{
		cJSON* extra_item = cJSON_CreateObject();
		cJSON_AddNumberToObject(extra_item, "frame_id", result->feature_list[i].frame_id);
		cJSON_AddNumberToObject(extra_item, "track_id", result->feature_list[i].track_id);
		cJSON_AddNumberToObject(extra_item, "left", result->feature_list[i].rect.left);
		cJSON_AddNumberToObject(extra_item, "right", result->feature_list[i].rect.right);
		cJSON_AddNumberToObject(extra_item, "top", result->feature_list[i].rect.top);
		cJSON_AddNumberToObject(extra_item, "bottom", result->feature_list[i].rect.bottom);

		cJSON* info_item = cJSON_CreateObject();
		cJSON_AddNumberToObject(info_item, "roll", result->feature_list[i].pose.roll);
		cJSON_AddNumberToObject(info_item, "pitch", result->feature_list[i].pose.pitch);
		cJSON_AddNumberToObject(info_item, "yaw", result->feature_list[i].pose.yaw);
		cJSON_AddNumberToObject(info_item, "blur", result->feature_list[i].blur);
		cJSON_AddItemToObject(extra_item, "info", info_item);

		//@ 可选的信息
		#if 0
		//设置框的颜色
		cJSON* color_item = cJSON_CreateObject();
		cJSON_AddNumberToObject(color_item, "b", 0);
		cJSON_AddNumberToObject(color_item, "g", 255);
		cJSON_AddNumberToObject(color_item, "r", 0);
		cJSON_AddItemToObject(extra_item, "color", color_item);

		//设置永远显示的字串
		cJSON* fixed_info_item = cJSON_CreateObject();
		cJSON_AddStringToObject(fixed_info_item, "id", "1234568");
		cJSON_AddItemToObject(extra_item, "fixed_info", fixed_info_item);
		#endif
		
		cJSON_AddItemToArray(extra_list_array, extra_item);
	}
	cJSON_AddItemToObject(request_obj, "extra", extra_list_array);
	
	json_print = cJSON_PrintUnformatted(request_obj); 

	FILE *fp = fopen("./result.json", "a");
	fprintf(fp, "%s\n", json_print);
	fclose(fp);
	
	ret = MGVL1_RET_OK;

EXIT:

	if(request_obj != NULL)
	{
		cJSON_Delete(request_obj);
	}
    if(json_print)
    {
        free(json_print);
    }

	DEBUG("############## out mgvl1_encode_message ################ !!!\n");

	return (int)ret;
}

