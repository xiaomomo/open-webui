import { WEBUI_API_BASE_URL } from '$lib/constants';

// 创建新的日记条目
export const createNewDiaryEntry = async (
	token: string,
	title: string,
	content: string
) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/diaries/create`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			title: title,
			content: content
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

// 获取所有日记条目
export const getDiaries = async (token: string = '') => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/diaries/`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

// 根据ID获取单个日记条目
export const getDiaryById = async (token: string, id: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/diary/${id}`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;

			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

// 更新日记条目
export const updateDiaryById = async (
	token: string,
	id: string,
	title: string,
	content: string
) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/diaries/${id}/update`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			title: title,
			content: content
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;

			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

// 删除日记条目
export const deleteDiaryById = async (token: string, id: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/diaries/${id}/delete`, {
		method: 'DELETE',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;

			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};