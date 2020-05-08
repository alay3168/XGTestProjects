import os

search_rets= [
            [
                {
                    "score": 0.12949040532112122,
                    "face_id": "3ec2f07a-4ccb-412e-93c3-670dfd41bc2c",
                    "person_id": "2e210481-bf4d-49bf-812f-6b5f8ef49760",
                    "capture_time": "2019-12-21T11:07:02",
                    "person_name": "zw"
                },
                {
                    "score": 0.12949040532112122,
                    "face_id": "5d6e9464-310f-4b8a-be69-f6cc46f0882c",
                    "person_id": "2e210481-bf4d-49bf-812f-6b5f8ef49760",
                    "capture_time": "2019-12-21T12:47:33",
                    "person_name": "zw"
                },
                {
                    "score": 0.12949040532112122,
                    "face_id": "f94c2523-fa81-445f-ab07-bbcf0e3f4827",
                    "person_id": "2e210481-bf4d-49bf-812f-6b5f8ef49760",
                    "capture_time": "2019-12-21T12:51:50",
                    "person_name": "zw"
                },
                {
                    "score": -0.05051083490252495,
                    "face_id": "a7f3567e-1e49-46c4-b746-b9879a9dceaf",
                    "person_id": "1579cf50-61f7-453d-a4c2-a5b263a944f4",
                    "capture_time": "2019-12-21T13:55:58",
                    "person_name": "11.jpg"
                },
                {
                    "score": -0.11600648611783981,
                    "face_id": "a6cfe09c-dbc7-40c0-9145-5dd6bcd15a16",
                    "person_id": "64ca18e4-0acb-4eec-95e0-6e5387d0cb28",
                    "capture_time": "2019-12-21T13:55:58",
                    "person_name": "query.jpg"
                }
            ]
        ]

print(search_rets[0][0]['score'])
print(search_rets[0][0]['person_name'])


li = [[1,2,3],
      [2,2,3],
      [1,'',''],
      [1,4,6],
      [6,4,4],
      [6, 4, 4],
      [6, '', ''],
      [6, '', ''],
      [6, 33, 55],
      [6, 33, 88],
      [6, 33, 88],
      [6, 33, 88],
      [6, 33, 4],
      ]

found_rets = [r for r in li if r[2]]
notfound_rets = [r for r in li if not r[2]]
ss = set([r[2] for r in found_rets])
print(found_rets)
print(notfound_rets)
print(ss)


#os.removedirs("D:\Desktop\gerify\gminute\CaptureImage")