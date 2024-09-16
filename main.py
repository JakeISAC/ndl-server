from face_detection import FaceDetection

if __name__ == '__main__':
    # new_encode = EncodeFaces("C:\\Users\\jakub\\PycharmProjects\\ndl\\authorized_faces\\images\\masha")
    # encode = new_encode.encode_face_file()
    # person = Person(id=uuid.uuid4(), name="Masha Ushakov",
    #                 images_path="C:\\Users\\jakub\\PycharmProjects\\ndl\\authorized_faces\\images\\masha",
    #                 authorization=AuthorizationStatus.AUTHORIZED, face_encodings=encode)
    # person.add(DatabaseOperations())
    # print(encode)

    # compare_faces = CompareFaces(encode["encodings"], encode["encodings"][0])
    # print(compare_faces.compare_faces())

    face_detection = FaceDetection()
    face_detection.start()
