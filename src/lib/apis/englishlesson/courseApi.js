import { WEBUI_API_BASE_URL } from '$lib/constants';

export async function fetchCourses() {
	try {
		const response = await fetch(`${WEBUI_API_BASE_URL}/fredisalesson/fredisalessons`);
		if (!response.ok) throw new Error('Failed to fetch courses');
		return await response.json();
	} catch (error) {
		console.error('Error fetching courses:', error);
		return [];
	}
}

export async function getLessonUnit(lessonUnitId) {
	try {
		console.log('getLessonUnit getLessonUnit lessonUnitId:' + lessonUnitId);
		const response = await fetch(`${WEBUI_API_BASE_URL}/fredisalesson/fredisalessons/${lessonUnitId}`);
		if (!response.ok) throw new Error('Failed to getLessonUnit');
		return await response.json();
	} catch (error) {
		console.error('Error fetching courses:', error);
		return [];
	}
}


export async function finishLessonUnitQA(userId, lessonId, userContent, learnStatus, token) {

	try {
		// 构建请求体数据
		const requestBody = {
			user_id: userId,
			lesson_id: lessonId,
			user_content: userContent,
			learn_status: learnStatus
		};

		// 发送POST请求
		const response = await fetch(`${WEBUI_API_BASE_URL}/userlesson/userlessons/create`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Accept': 'application/json',
				authorization: `Bearer ${token}`
			},
			body: JSON.stringify(requestBody)
		});

		// 检查请求是否成功
		if (response.ok) {
			console.log("finishUnitQA success")
		} else {
			console.error(`Request failed with status ${response.status}`);
		}
	} catch (err) {
		console.error(`Request failed with status ${err.message}`);
	}
}
