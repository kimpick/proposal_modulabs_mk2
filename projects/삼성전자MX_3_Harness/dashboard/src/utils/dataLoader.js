// src/utils/dataLoader.js
// Vite의 import.meta.glob를 사용하여 상위 폴더의 모든 content.json을 가져옵니다.

export const loadCurriculums = () => {
  // ../../../은 현재 폴더(src/utils)에서 삼성전자MX_3_Harness 디렉토리를 가리킵니다.
  // dashboard 폴더 외부의 파일도 빌드 시 포함됩니다. (vite.config.js 설정 필요)
  const modules = import.meta.glob('../../../*/content.json', { eager: true });
  
  const curriculums = [];
  
  for (const path in modules) {
    const data = modules[path].default || modules[path];
    
    // 경로에서 폴더명 추출 (예: "../../../4월_에이전틱코딩_발전/content.json" -> "4월_에이전틱코딩_발전")
    const parts = path.split('/');
    const folderName = parts[parts.length - 2] || '';
    
    // 4월(개발자), 5월(비개발자) 카테고리화
    const month = folderName.includes('4월') ? '4월' : '5월';
    const type = month === '4월' ? 'Developer' : 'Non-Developer';
    
    curriculums.push({
      id: folderName, // 폴더명을 고유 ID로 사용
      folderName,
      month,
      type,
      ...data,
    });
  }
  
  // 정렬 (4월 먼저, 그 다음 5월. 폴더명 기준)
  return curriculums.sort((a, b) => a.folderName.localeCompare(b.folderName));
};
